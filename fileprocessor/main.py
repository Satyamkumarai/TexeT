from pymongo import MongoClient
import pymongo
from bson.objectid import ObjectId
import time 
from settings import username,password,dbname
from constants import FileStatus
from time import sleep
DELAY_INTERVAL = 5 
MAX_RETRIES = 5

client = None
db = None
collection = None




def initState(currentState):
    """Create the DB connection"""
    global client , db , collection
    client = MongoClient(f"mongodb+srv://{username}:{password}@cluster0.70rhn.mongodb.net/{dbname}?retryWrites=true&w=majority")
    print(f"mongodb+srv://{username}:{password}@cluster0.70rhn.mongodb.net/{dbname}?retryWrites=true&w=majority")
    db = client.texet
    collection = db.queue
    return 'busy'

def busyState(currentState):
    # get a doc from the queue 
    # if doc not empty ?
        # do processing 
        # return 'busy'
    return 'wait'

def waitState(currentState):
    retries = 0
    delay = DELAY_INTERVAL
    while retries < MAX_RETRIES:
        pass 
        # fetch a doc from the queue
        # if doc not empty ?
            # return 'busy'
        # else:
            # time.sleep(delay)
    return 'watch'

def watchState(currentState):
    # create a watch stream checking for inserts.
    # insert Occurs?
    # time.sleep(randInt(1,5))
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
            
