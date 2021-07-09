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


DELAY_INTERVAL = 0.1
MAX_RETRIES = 5
INSTANCE_DIR = "../webserver/instance"
client = None
db = None
collection = None

def do_work(work):
    uploaddir = work.get('input')
    downloaddir = work.get('output')
    filename = work.get('uuid')
    print(work)  #DEBUG
    uploaddir = os.path.join(INSTANCE_DIR,uploaddir)
    downloaddir = os.path.join(INSTANCE_DIR,downloaddir)
    print(uploaddir,downloaddir,"upload dir amd download dir")  #DEBUG
    up_file = os.path.join(uploaddir, filename+".pdf")
    down_file = os.path.join(downloaddir, filename+'-download.pdf')
    ocrmypdf_args = ["ocrmypdf","--force-ocr", up_file, down_file]
    proc = run(ocrmypdf_args, stdout=PIPE, stderr=PIPE, encoding="utf-8")
    if proc.returncode != 0:
        print("Error Occured While running OCR") #DEBUG
    else:
        print(f"processed {down_file}")  #DEBUG




def initState(currentState):
    """Create the DB connection"""

    global client , db , collection

    print("<<INIT>>")#DEBUG
    print(f"mongodb+srv://{username}:{password}@cluster0.70rhn.mongodb.net/{dbname}?retryWrites=true&w=majority")
    connected = False
    client = None
    while not connected:
        client = MongoClient(f"mongodb+srv://{username}:{password}@cluster0.70rhn.mongodb.net/{dbname}?retryWrites=true&w=majority")
        connected = not  client == None

    db = client.texet
    collection = db.queue
    print(collection)
    return 'busy'







def busyState(currentState):

    global collection,client ,db

    print("<<BUSY>>")#DEBUG

    #get a document and setIts startTime 
    pdf_work_ensure_params = {"startTime":None,"image":False}
    work = collection.find_one_and_update(pdf_work_ensure_params,{'$set':{'startTime':datetime.utcnow()}},sort=[('createdOn',pymongo.ASCENDING)])
    if work:
        work_id = ObjectId(work.get('_id'))
        try:
            do_work(work)
            collection.find_one_and_update({"_id":work_id},{'$set':{'endTime':datetime.utcnow()}})
        except:
            collection.find_one_and_update({"_id":work_id},{'$set':{'endTime':datetime.utcnow(),'error':True}})
            print("Error Occured ",work_id)            
        return 'busy'
    print("Error finding work ..Switching to waitState") # DEBUG
    return 'wait'

def waitState(currentState):
    global collection,client ,db
    print("<<WAIT>>")   #DEBUG
    retries = 0
    delay = DELAY_INTERVAL
    while retries < MAX_RETRIES:
        print("Current Try ",retries+1) #DEBUG
        pdf_work_ensure_params = {"startTime":None,"image":False}
        work = collection.find_one_and_update(pdf_work_ensure_params,{'$set':{'startTime':datetime.utcnow()}},sort=[('createdOn',pymongo.ASCENDING)])
        if work:
            return 'busy'
        else:
            retries+=1
            time.sleep(delay)

    return 'watch'

def watchState(currentState):
    print("<<WATCH>>") #DEBUG
    print("Waiting for document Inserts ") #DEBUG
    for insert_work in collection.watch([{"$match":{'operationType':"insert"}}]):
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
            time.sleep(randint(1,5))
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
            
