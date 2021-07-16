from pymongo import MongoClient
import pymongo
from bson.objectid import ObjectId
import time 
from settings import username,password,dbname
from time import sleep
from datetime import datetime
import os
import json
import shlex
from subprocess import PIPE, run
from random import randint
from convert import extract_pages,convert_to_pdf
from schema import Task,TaskData

DELAY_INTERVAL = 0.1
MAX_RETRIES = 5
INSTANCE_DIR = "../webserver/instance"
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
        uploaddir = os.path.join(INSTANCE_DIR,uploaddir)
        downloaddir = os.path.join(INSTANCE_DIR,downloaddir)
        print(uploaddir,downloaddir,"upload dir amd download dir")  #DEBUG
        up_file = os.path.join(uploaddir, filename)
        down_file = os.path.join(downloaddir, filename+'.pdf')
        try:
            extract_pages(up_file)
            convert_to_pdf(up_file,down_file)
        except Exception as  e:
            print("ERROR",e)

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
    image_work_ensure_params = {"startTime":None,"image":True}
    work = db.queue.find_one_and_update(image_work_ensure_params,{'$set':{'startTime':datetime.utcnow()}},sort=[('createdOn',pymongo.ASCENDING)])
    if work:
        work_id = ObjectId(work.get('_id'))
        try:
            # get the corresponding work_data 
            work_data = db.data.find_one({"task":work_id})
            # process the images and convert them to pdf
            do_work(work_data)
            
            #create a new pdf task from old image task
            new_pdf_task = Task.pdf_task_from_image_task_dict(work,work_data)
            new_pdf_task_data = new_pdf_task.taskData

            # delete the old image task
            db.queue.delete_one({"_id":ObjectId(work.get("_id"))})
            db.data.delete_one({"_id":ObjectId(work_data.get("_id"))})
            print("deleted old tasks ")

            # insert the  new pdf task with correct task data
            db.queue.insert_one(new_pdf_task.to_dict())
            db.data.insert_one(new_pdf_task_data.to_dict())
            print("inserted new tasks :")



        except Exception as e:
            # mark the work as complete and the error flag
            db.queue.find_one_and_update({"_id":work_id},{'$set':{'endTime':datetime.utcnow(),'error':True}})
            print("Error Occured ",e)            
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
        image_work_ensure_params = {"startTime":None,"image":True}
        work = db.queue.find_one(image_work_ensure_params,sort=[('createdOn',pymongo.ASCENDING)])
        if work:
            print("found work in wait :",work)
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
        if not  doc.get('image') : #if the insert type is not  image continue
            print("pdf type ignoring ..") #DEBUG
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
            
