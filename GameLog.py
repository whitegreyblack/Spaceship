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

    def __init__(self, maxsize=1000):
        self.messages=[]
        self.maxsize = maxsize
        self.index = 0

    def add(self, message):
        if len(self.messages)+1 > self.maxsize:
            self.dump(self.message[0])
            self.messages.pop(0)
        self.messages.append(message)

    def update(self, n = 0):
        self.index = len(self.messages)-4 if not n else n

    def write(self, message):
        """Return a set of messages for game loop to print"""
            return log(self.messages[self.index+i] for i in range(4))

    def dump(self, f):
        """Write log to disk"""
