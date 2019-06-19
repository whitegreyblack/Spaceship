# system.py

"""Base system class"""

class System(object):
    def __init__(self, engine):
        # reference to the engine object
        self.engine = engine

    @classmethod
    def classname(cls):
        return cls.__name__.lower()

    def process(self):
        raise NotImplementedError("Implement base system process method")
