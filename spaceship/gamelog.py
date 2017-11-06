import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))+'/../')
from collections import namedtuple
from time import ctime, clock
"""Implements the Game Logger used in displaying messages to the terminal
Basic Usage:
    After instantiation at global/main file level, calls to GameLogger should
    be only to append to the 
Implementation Details:
    I want the class to be completely seperated from bearlibterminal. This
    will allow for a more independent object structure. Calls to gamelogger
    should only be the following commands:
        -   adding messages to the stack
        -   returning the next n messages for terminal output
        -   writing messages to filetype of choice
        -   ?should it update index dynamically or manually?
"""

statement = namedtuple("Statement", "statement ctime clock")

log = namedtuple("Logger", "messages")

class GameLogger:
    """
    Variables:

        @messages : list used as a queue

        @maxsize  : the number of messages kept on queue

        @index    : the pointer to the first message to be printed - usually fourth from the end
        
        @counter  : the increment variable if duplicate messages are encountered

        Methods: {add, update, write, dump, dumps}
    """

    def __init__(self, screenlinelimit, ptt=False):
        """
        @args: 
            screenlinelimit(required) -- specify number of lines to be shown on screen
            ptt(position) -- specify if messages are printed to terminal
            maxsize(positional) -- can specify the nubmer of items in queue before erasure
        """
        self.index = 0
        self.counter = 0
        self.messages = []
        self.print_to_term = ptt
        self.maxlines = screenlinelimit
        self.setupFileWriting()

    def print_on(self):
        '''Toggles print to terminal on; shows message if already on'''
        if self.print_to_term:
            print("Gamelogger-Printing is already enabled")
        else:
            self.print_to_term = True

    def print_off(self):
        '''Toggles print to terminal off; shows message if already off'''
        if not self.print_to_term:
            print("Gamelogger-Printing is already disabled")
        else:
            self.print_to_term = False

    def print_once(self, message):
        self.print_on()
        self.add(message)
        self.print_off()

    def setupFileWriting(self):
        '''Adds the filename attribute to class for use in message log recording'''
        if not os.path.isdir('logs'):
            print('Log folder does not exist -- Creating "./logs')
            os.makedirs('logs')

        self.filename = "logs/log_"+"_".join(filter(lambda x: ":" not in x, ctime().split(" ")))+".txt"
        print("Setup log file in {}".format(self.filename))
        
        # open it once to see if error is raised
        with open(self.filename, 'w') as f:
            pass

    def getHeader(self):
        '''Returns a time string for use in log pre-messages'''
        return "["+"-".join(filter(lambda x: ":" in x, ctime().split(" ")))+"] :- "

    def add(self, message):
        """Adds a message to queue and handles repeated messages from game"""
        # checks terminal print flag
        if self.print_to_term:
            print(message)

        # Checks if message is the same as before
        if self.messages and message in self.messages[-1]:
            self.messages.pop(-1)
            self.counter += 1
            message += "(x{})".format(self.counter)
        else:
            self.counter = 0
        
        # Dump the messages as long as they are not repeats of the same message
        if len(self.messages) + 1 > self.maxlines:
            if self.counter: # don't need to repeatedly dump the same message every time
                self.dump(self.messages.pop(0))

        self.messages.append(message)
        self.update()

    def update(self, n=0):
        """Updates the points to the message position to start printing from"""
        self.index = len(self.messages)-self.maxlines if not n else n

    def write(self):
        """Return a set of messages for game loop to print"""
        if len(self.messages) < self.maxlines:
            return log(self.messages)

        return log([self.messages[self.index+i] for i in range(self.maxlines)])

    def dump(self, message):
        """Write log to disk"""
        try:
            with open(self.filename, 'a') as f:
                f.write(self.getHeader() + message + "\n")

        except OSError:
            with open(self.filename, 'w') as f:
                f.write(self.getHeader() + message + "\n")

        except:
            raise

    def dumps(self):
        """Write entire message queue to disk"""
        print("writing dump to {}".format(self.filename))
        # with open(self.filename, 'a') as f:
        for message in self.messages:
                # f.write(self.getHeader() + message + "\n")
            self.dump(message)

