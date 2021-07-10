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
TTL_INDEX_EXPIRE_TIME = 20 # Need To change this ..
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
    print(collection)#DEBUG
    ttl_endTime_index = collection.create_index([("endTime",1)],expireAfterSeconds=TTL_INDEX_EXPIRE_TIME)
    for index in collection.list_indexes():
        print(index)
    return 'watch'

def watchState(currentState):
    print("<<WATCH>>") #DEBUG
    print("Waiting for document deletes") #DEBUG
    for delete_work in collection.watch([{"$match":{'operationType':"delete"}}]):
        print(delete_work)
        doc = delete_work['documentKey']
        print(doc)

states = {
    'init':initState,
    'watch':watchState
}



if __name__=='__main__':
    #start state
    startState = states['init']
    currentState = startState
    nextState = startState(currentState)
    while 1 :
        nextState = states[nextState](nextState)
            
