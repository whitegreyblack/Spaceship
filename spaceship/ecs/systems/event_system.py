# event_system

"""Event     system class"""

class EventSystem(object):
    def __init__(self, engine):
        # reference to the engine object
        self.engine = engine

    @classmethod
    def classname(cls):
        return cls.__name__.lower()

    def process(self):
