#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jul  7 11:39:10 2017

@author: kadu
"""

import numpy as np
import sys, os, traceback

class ExceptionFSM(Exception):

    """This is the FSM Exception class."""

    def __init__(self, value):
        self.value = value

    def __str__(self):
        return self.value
    
class FiniteStatesMachine(object):
    """Class implements a Finite State Machine methods for state and transitions.
    The possible states are: stopped(0), started(1), collecting(2) and processing(3)""" 
    
    def __init__(self, initialState, memoryState=None):
        # Map (current_state, input_symbol) --> (action, next_state)
        self.stateTransitions = {}
        
        self.defaultTransition = None
        self.inputSymbol = None
        self.action = None
        self.nextState = None
        
        self.initialState = 'stopped'
        self.currentState = 'stopped'
        self.randomArray = []
        self.memoryState = memoryState
    
    def getPreviousState(self):
        # check for empty array
        if len(self.memoryState) > 0:
           return self.memoryState.pop()
       
        else:
            return "stopped"
    
    def getCurrentState(self):
        return self.currentState
    
    def setCurrentState(self, currentState):
        self.currentState = currentState
        
    def setPreviousState(self, currentState):
        self.memoryState.append(currentState)
    
    def reset (self):

        """Sets the current_state to the initial_state (0) and sets
        input_symbol to None. """

        self.currentState = self.initialState
        self.inputSymbol = None
    
    def addTransitionList (self, inputSymbol, state, action=None, nextState=None):

        """Adds the transition to a list of input symbols. The list is mapped as follows:
        (inputSymbol, state), (action, nextState), where 'inputSymbol' is the input provided
        by the user, 'state' is the current state of the FSM, 'action' is a function to be
        executed and 'nextState' is the next state of the FSM after the success of the action.

        The action may be a transition function or a generic info function about the state of
        the FSM. """

        if nextState is None:
            nextState = state
        
        self.stateTransitions[(inputSymbol, state)] = (action, nextState)
    
    def setDefaultTransition (self, action, nextState):

        """This sets the default transition. This defines an action and
        next_state if the FSM cannot find the input symbol provided by the user
        and the current state in the transition list.

        The default transition can be removed by setting the attribute
        defaultTransition to None. In this case, for default the nextState will be 
        the current state of the FSM."""
        
        if nextState is not None:
           self.defaultTransition = (action, nextState)
        else:
           self.defaultTransition = (action, self.initialState)
    
    def getTransition (self, inputSymbol, state):

        """This method returns the tuples (action, next state) given an inputSymbol
        and state.

        The sequence to check for a defined transition goes as follows:

        1. Check stateTransitions[] that match exactly the tuple,
            (inputSymbol, state)

        2. Check if the defaultTransition is defined.
            This catches any inputSymbol and any state.
            This is a handler for errors, undefined states, or defaults.

        3. If no transition was defined, then raise an exception.
        """

        if (inputSymbol, state) in self.stateTransitions:
            return self.stateTransitions[(inputSymbol, state)]
        elif self.defaultTransition is not None:
            return self.defaultTransition
        else:
            raise ExceptionFSM ('Transition is undefined: (%s, %s).' %
                (str(inputSymbol), str(state)) )
    
    def process (self, inputSymbol):

        """This is the main method that process user input. This cause the FSM to
        change state and call an action. This method calls getTransition() to find 
        the correct action and nextState associated with the inputSymbol and 
        currentState. This method processes one complete input symbol."""
        
        self.inputSymbol = inputSymbol
        (self.action, self.nextState) = self.getTransition (self.inputSymbol, self.currentState)
        
        if self.action is not None:
            self.action (self)
        
        self.memoryState.append(self.currentState)
        self.currentState = self.nextState
        self.nextState = None


# transition actions    
def collectData(f):
    
    f.randomArray = np.random.randint(0, 9, size=(3, 3))

def processData(f):
    
    # multiply the array by the scalar 5
    f.randomArray = [x * 5 for x in f.randomArray]
    
    # get the transposed result from 2d array
    f.randomArray = np.transpose(f.randomArray)
    
    print ('\n'.join(map(str, f.randomArray)))

def stopFSM(f):
    f.initialState = 'stopped'
    f.previousState = 'stopped'
    f.currentState = 'stopped'
    f.randomArray = []
    
    
def starFSMVariables(f):
    f.initialState = 'stopped'
    f.previousState = 'stopped'
    f.currentState = 'stopped'
    f.randomArray = []
    

def Error (f):
    print ('The tuple (' + f.inputSymbol + ', ' + f.getCurrentState()+ ') was not founded')
    print ('FSM was moved to the initial state')
    
    
def main():

    """Here the FSM is stared and the state transitions are defined."""
    

    f = FiniteStatesMachine('stopped', [])
    f.setDefaultTransition(Error, None)
    
    f.addTransitionList('start',    'stopped',     starFSMVariables,  'started')
    f.addTransitionList('collect',  'started',     collectData,       'collecting')
    f.addTransitionList('collect',  'processing',  collectData,       'collecting')
    f.addTransitionList('stop',     'started',     stopFSM,              'stopped')
    f.addTransitionList('process',  'collecting',  processData,       'processing')
    f.addTransitionList('stop',     'collecting',  stopFSM,              'stopped')
    f.addTransitionList('stop',     'processing',  stopFSM,              'stopped')
    
    f.addTransitionList('start',    'stopped',     starFSMVariables,  'started')
    
    
    print('This is a Finite Machine State system')
    print('You can change the FSM state by sending an input to the system')
    print('The possible states are: started, collecting, processing and stopped')
    print('Different inputs cause a state change in the FSM')
    print('The possible inputs are: start, collect, process and stop')
    print('You can also check for the current and previous state of the FSM')
    print('The possible inputs for this case are: current and previous')
    print('The initial state of the FSM system is stopped')
    print('Please, provide an input for the FSM system')
    
    inputstr = ""
    
    while inputstr != "exit":
        inputstr = input('> ')
        
        if inputstr != "exit":
            
            if inputstr == "current":
                print(f.getCurrentState())
                
            elif inputstr == "previous":
                print(f.getPreviousState())
                
            else:
                f.process(inputstr)
            
                if inputstr == "process":
                   # After process go the 'collecting' state again
                   f.process('collect')
            
    
if __name__ == '__main__':
    try:
        main()
        sys.exit(0)
        
    except KeyboardInterrupt as e:
        raise e
    except SystemExit as e:
        raise e
    except Exception as e:
        print ('ERROR, UNEXPECTED EXCEPTION')
        print (str(e))
        traceback.print_exc()
        os._exit(1)
    
    