# action_queue.py

"""An event queue for all actions that can be performed by entities"""

 
class ActionQueue(object):
    def __init__(self, logger):
        self.logger = logger

    def add_action(self, name, action):
        self.__setattr__(name, action)

    def onRecieve(self, action):
        if action.name == 'move':
            move()
