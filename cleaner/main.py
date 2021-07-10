from pymongo import MongoClient
import pymongo
from bson.objectid import ObjectId
import time 
from settings import username,password,dbname
from time import sleep
from datetime import datetime
import os
import json
import shutil

INSTANCE_DIR = "../webserver/instance"
client = None
db = None

def delete_files(work_data):
    if work_data:
        uploaddir = work_data.get('input')
        downloaddir = work_data.get('output')
        uuid = work_data.get('uuid')
        print(work_data)  #DEBUG
        uploaddir = os.path.join(INSTANCE_DIR,uploaddir)
        downloaddir = os.path.join(INSTANCE_DIR,downloaddir)
        print(uploaddir,downloaddir,"upload dir amd download dir",sep='\n')  #DEBUG
        image = work_data.get('image')
        if image:
            # if image type doc delete (Delete the uploaded images)
            up_dir = os.path.join(uploaddir, uuid)
            down_dir = os.path.join(downloaddir, uuid)
            try:
                # remove the images dir
                print("Removing up_dir",up_dir) # DEBUG
                shutil.rmtree(up_dir)
                print("done")
            except Exception as e:
                print(e)
                
        else:
            up_file = os.path.join(uploaddir, uuid+'.pdf')
            down_file = os.path.join(downloaddir, uuid+'-download.pdf')
            try:
                print("removing file",up_file)
                os.remove(up_file)
                print("done")
            except Exception as e:
                print(e)
                print("Error deleting file ",up_file) #DEBUG
                pass
            try:
                print("removing file",down_file)
                os.remove(down_file)
                print("done")
            except Exception as e:
                print(e)
                print("Error deleting file ",up_file) #DEBUG
            # if pdf type task deleted:



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
    return 'watch'

def watchState(currentState):
    print("<<WATCH>>") #DEBUG
    print("Waiting for document deletes") #DEBUG
    for delete_work in db.queue.watch([{"$match":{'operationType':"delete"}}]):
        print(delete_work)
        work_doc_id = delete_work['documentKey']['_id']
        # mark the work_data doc for deletion 
        work_data_doc = db.data.find_one_and_update({"task":ObjectId(work_doc_id)},{"$set":{"deleted":datetime.utcnow()}})
        # delete the local file 
        delete_files(work_data_doc)
        


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
            
