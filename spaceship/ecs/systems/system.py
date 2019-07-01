# system.py

"""Base system class"""

class System(object):
    def __init__(self, engine, logger=None):
        # reference to the engine object
        self.engine = engine
        # need a logger listener here that appends to self.engine.logger
        self.logger = logger

    @classmethod
    def classname(cls):
        return cls.__name__.lower()

    def process(self):
        raise NotImplementedError("Implement base system process method")
