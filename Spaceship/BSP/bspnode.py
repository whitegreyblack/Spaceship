import numpy
import random
import pprint

class BSPNode:
    def __init__(self, v, x=False, y=True):
        self.x = x
        self.y = y
        self.v = v
        self.l = 0
        self.r = 0
        self.p = 0
    def __repr__(self):
        if self.x:
            return "{}('X':{})".format(self.__class__.__name__, self.v)
        else:
            return "{}('Y':{})".format(self.__class__.__name__, self.v)
