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

    def __init__(self, maxsize=1000):
        """@args: maxsize(positional) -- can specify the nubmer of items in queue before erasure"""
        self.messages=[]
        self.maxsize = maxsize
        self.index = 0
        self.counter = 0

    def add(self, message):
        """Adds a message to the stack
        Walkthrough: 
            Checks if message is the same as before
            If it is then appends a number (xN) to the message until message is different
            if not, then checkks the stack for maxsize and removes the topmost element from queue
            Finally appends the new message to stack and updates pointer
        """
        if self.messages and message in self.messages[-1]:
            self.messages.pop(-1)
            print("same message")
            self.counter += 1
            message += f'(x{self.counter})'
        else:
            self.counter = 0
        
        if len(self.messages) + 1 > self.maxsize:
            self.dump(self.messages[0])
            self.messages.pop(0)

        self.messages.append(message)
        self.update()
    def update(self, n=0):
        """Updates the points to the message position to start printing from"""
        self.index = len(self.messages)-4 if not n else n

    def write(self):
        """Return a set of messages for game loop to print"""
        if len(self.messages) < 4:
            return log(self.messages)
        return log([self.messages[self.index+i] for i in range(4)])

    def dump(self, message):
        """Write log to disk -- TODO: Unneeded? Just use dumps?"""
        filename = "logs/log_"+"_".join(filter(lambda x: x != "", ctime().split(" ")))+".txt"
        header = "["+"-".join(filter(lambda x: x != "", ctime().split(" ")))+"]:- "
        with open(filename, 'a') as f:
            f.write(header + message)
            
    def dumps(self):
        """Write entire message queue to disk"""
        clock = "_".join(filter(lambda x: x != "", ctime().split(" ")))
        filename = "logs/log_"+clock+".txt"
        print(f'writing to {filename}')
        with open(filename, 'a') as f:
            for message in self.messages:
                clock = "_".join(filter(lambda x: x != "", ctime().split(" ")))
                header = f'["+{clock}+"]:- '
                f.write(header + message)

