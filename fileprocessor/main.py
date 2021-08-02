from pymongo import MongoClient
import pymongo
from bson.objectid import ObjectId
import time 
from settings import username,password,dbname,INSTANCE_FOLDER
from time import sleep
from datetime import datetime
import os
import json
import shlex
from subprocess import PIPE, run
from random import randint


DELAY_INTERVAL = 0.1
MAX_RETRIES = 5
# INSTANCE_FOLDER = "../webserver/instance"
TTL_INDEX_EXPIRE_TIME = 30 # Need To change this ..
client = None
db = None

def do_work(work_data):
    # if work_data is None raise Exception
    if work_data:
        uploaddir = work_data.get('input')
        downloaddir = work_data.get('output')
        filename = work_data.get('uuid')
        print(work_data)  #DEBUG
        uploaddir = os.path.join(INSTANCE_FOLDER,uploaddir)
        downloaddir = os.path.join(INSTANCE_FOLDER,downloaddir)
        print(uploaddir,downloaddir,"upload dir amd download dir")  #DEBUG
        up_file = os.path.join(uploaddir, filename+".pdf")
        down_file = os.path.join(downloaddir, filename+'-download.pdf')
        ocrmypdf_args = ["ocrmypdf","--force-ocr", up_file, down_file]
        proc = run(ocrmypdf_args, stdout=PIPE, stderr=PIPE, encoding="utf-8")
        if proc.returncode != 0:
            print("Error Occured While running OCR") #DEBUG
            raise Exception("Failed To process pdf")
        else:
            print(f"processed {down_file}")  #DEBUG
    else:
        raise Exception("Invalid Workdata")



def initState(currentState):
    """Create the DB connection"""

    global client , db 

    print("<<INIT>>")#DEBUG
    print(f"mongodb+srv://{username}:{password}@cluster0.70rhn.mongodb.net/{dbname}?retryWrites=true&w=majority")
    connected = False
    client = None
    while not connected:
        client = MongoClient(f"mongodb+srv://{username}:{password}@cluster0.70rhn.mongodb.net/{dbname}?retryWrites=true&w=majority")
        connected = not  client == None
    db = client.texet

    # Indicies on the db.queue collection
    # 1. createdOn < Sort index >    -> To get the FIFO
    # 2. taskData  < sort index >    -> While dowloading a file get task from task_data
    # 3. endTime   < TTL  index >    -> To delete the doc after say 24 h
    createdOn_index = db.queue.create_index([("createdOn",1)])
    taskData_index = db.queue.create_index([("taskData",1)])
    endTime_index = db.queue.create_index([("endTime",1)],expireAfterSeconds=TTL_INDEX_EXPIRE_TIME)

    # Indicies on the db.data collection 
    # 1. uuid < sort index >        -> Download pdf direct uuid
    # 2. task < sort index >        -> Cleaner get the task_data from task._id 
    # 3. deleted < TTL index >      -> Auto delete task_data  (0 s)
    uuid_index = db.data.create_index([("uuid",1)])
    task_index = db.data.create_index([("task",1)])
    deleted_index = db.data.create_index([("deleted",1)],expireAfterSeconds=0)

    #DEBUG
    print("queue Indicies")
    for index in db.queue.list_indexes():
        print(index)
    print("Data Indicies")
    for index in db.data.list_indexes():
        print(index)
    return 'busy'







def busyState(currentState):

    global client ,db

    print("<<BUSY>>")#DEBUG

    # Get a pdf type work with null startTime
    pdf_work_ensure_params = {"startTime":None,"image":False}
    work = db.queue.find_one_and_update(pdf_work_ensure_params,{'$set':{'startTime':datetime.utcnow()}},sort=[('createdOn',pymongo.ASCENDING)])
    if work:
        work_id = ObjectId(work.get('_id'))
        try:
            # get the corresponding work_data 
            work_data = db.data.find_one({"task":work_id})
            # process the file 
            do_work(work_data)
            # mark  the work as complete
            db.queue.find_one_and_update({"_id":work_id},{'$set':{'endTime':datetime.utcnow()}})
        except:
            # mark the work as complete and the error flag
            db.queue.find_one_and_update({"_id":work_id},{'$set':{'endTime':datetime.utcnow(),'error':True}})
            print("Error Occured ",work_id)            
        return 'busy'
    print("Error finding work ..Switching to waitState") # DEBUG
    return 'wait'

def waitState(currentState):
    global client ,db
    print("<<WAIT>>")   #DEBUG
    retries = 0
    delay = DELAY_INTERVAL
    while retries < MAX_RETRIES:
        print("Current Try ",retries+1) #DEBUG
        pdf_work_ensure_params = {"startTime":None,"image":False}
        work = db.queue.find_one(pdf_work_ensure_params,sort=[('createdOn',pymongo.ASCENDING)])
        if work:
            return 'busy'
        else:
            retries+=1
            time.sleep(delay)

    return 'watch'

def watchState(currentState):
    print("<<WATCH>>") #DEBUG
    print("Waiting for document Inserts ") #DEBUG
    for insert_work in db.queue.watch([{"$match":{'operationType':"insert"}}]):
        print(insert_work)
        doc = insert_work['fullDocument']
        print(doc)
        if doc.get('image') : #if the insert type is image continue
            print("image type ignoring ..") #DEBUG
            continue
        else:
            if doc.get('startTime'):
                print('already in progress .. ignoring...') #DEBUG
                continue
            time.sleep(1)
            return 'busy'

states = {
    'init':initState,
    'busy':busyState,
    'wait':waitState,
    'watch':watchState
}



if __name__=='__main__':
    #start state
    startState = states['init']
    currentState = startState
    nextState = startState(currentState)
    while 1 :
        nextState = states[nextState](nextState)
            
