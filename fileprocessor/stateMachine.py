
#The States ..
count = 0
def initState(currentState):
    print("init ")
    return 'busy'

def busyState(currentState):
    global count 
    print("busy-->%d"%count)
    count+=1
    return 'wait'

def waitState(currentState):
    print("wait")
    return 'watch'

def watchState(currentState):
    print('watch')
    global count
    if count < 5:
        return 'busy'
    return 'end'

states = {
    'init':initState,
    'busy':busyState,
    'wait':waitState,
    'watch':watchState
}

#start state
startState = states['init']
currentState = startState
nextState = startState(currentState)
while 1 :
    if nextState!='end':
        nextState = states[nextState](nextState)
    else:
        break
            
