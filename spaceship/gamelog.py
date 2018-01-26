import os
import sys
import textwrap
from time import ctime, clock
from collections import namedtuple
from bearlibterminal import terminal as term
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

log = namedtuple("Logger", "message color")

class GameLogger:
    """
    Variables:

        @messages : list used as a queue

        @maxsize  : the number of messages kept on queue

        @index    : the pointer to the first message to be printed - usually fourth from the end
        
        @counter  : the increment variable if duplicate messages are encountered

        Methods: {add, update, write, dump, dumps}
    """

    def __init__(self, width, screenlinelimit, footer, ptt=False):
        """
        @args: 
            screenlinelimit(required) -- specify number of lines to be shown on screen
            ptt(position) -- specify if messages are printed to terminal
            maxsize(positional) -- can specify the nubmer of items in queue before erasure
        """
        self.index = 0
        self.counter = 0
        self.messages = []
        self.width = width
        self.print_to_term = ptt
        self.height = screenlinelimit
        self.setupFileWriting(footer)

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

    def setupFileWriting(self, footer):
        '''Adds the filename attribute to class for use in message log recording
        '''
        if not os.path.isdir('logs'):
            print('Log folder does not exist -- Creating "./logs"')
            os.makedirs('logs')

        self.last_message = ""
        self.filename = "logs/log_" + self.date() + footer + ".txt"
        self.filename = self.filename.replace('__', '_')
        print("Setup log file in {}".format(self.filename))
        
        # open it once to see if error is raised
        with open(self.filename, 'a') as f:
            pass

    def date(self):
        return "_".join(filter(lambda x: ":" not in x, ctime().split(" ")))

    def time(self):
        return "-".join(filter(lambda x: ":" in x, ctime().split(" ")))

    def getHeader(self):
        '''Returns a time string for use in log pre-messages'''
        return "[" + self.time() + "] :- "

    def add(self, message, color):
        """Adds a message to queue and handles repeated messages from game"""
        def add_message(message):
            # checks terminal print flag
            if self.print_to_term:
                print(message)

            # Checks if messages are in the queue and if message is the same 
            # as before
            if self.messages and message == self.last_message:
                # print('counter')
                self.messages.pop(-1)
                self.counter += 1

                # save the unaltered message for comparison
                self.last_message = message            
                message += "(x{})".format(self.counter)

            else:
                # print('reset')
                self.counter = 0
                self.last_message = message            

            # Dump the messages as long as they are not repeats of the same 
            # message
            if len(self.messages) + 1 > self.height:
                # print('dump')
                # don't need to repeatedly dump the same message every time
                if not self.counter:
                    self.dump(self.messages.pop(0))

            self.messages.append([self.getHeader(), message, color])
            self.update()

        messages = textwrap.wrap(message, width=self.width - 2)
        for msg in messages:
            add_message(msg)

    def update(self, n=0):
        """Updates the points to the message position to start printing from"""
        self.index = len(self.messages) - self.height if not n else n

    def draw(self, log=None, color="white", refresh=True):
        if log:
            self.add(log, color)
        
        self.clear()
        messages = self.write()
        for index, msg in enumerate(messages):
            term.puts(
                x=term.state(term.TK_WIDTH) - self.width,
                y=term.state(term.TK_HEIGHT) - self.height + index - 1,
                s="[c={}]{}[/c]".format(msg.color, msg.message))
        
        if refresh:
            term.refresh()

    def clear(self):
        term.clear_area(0, 
                        term.state(term.TK_HEIGHT) - self.height - 1, 
                        term.state(term.TK_WIDTH), 
                        self.height + 1)

    def write(self):
        """Return a set of messages for game loop to print"""
        if len(self.messages) < self.height:  
            return [log(message[1], message[2]) for message in self.messages]
            # return log(self.messages, )

        return [log(self.messages[i][1], self.messages[i][2])
                for i in range(self.height)]

    def dump(self, message):
        """Write log to disk"""
        # transform list into string
        message = "".join(message)
        try:
            with open(self.filename, 'a') as f:
                f.write(message + "\n")

        except OSError:
            with open(self.filename, 'w') as f:
                f.write(message + "\n")

        except:
            raise

    def dumps(self):
        """Write entire message queue to disk"""
        # print("writing dump to {}".format(self.filename))
        # with open(self.filename, 'a') as f:
        for message in self.messages:
                # f.write(self.getHeader() + message + "\n")
            self.dump(message)
        self.messages = []

