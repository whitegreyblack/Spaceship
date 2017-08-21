import numpy
import random
import pprint
import bspnode

class BSPTree:
    def __init__(self, x, y):
        self.r = None
        self.n = 0
        self.x = x
        self.y = y
    def add(self):
        if not self.r:
            self.r = bspnode.BSPNode(self.y//2)
        else:
            clk = 1
            t = self.r
            p = self.r

