from imports import *

class Color:
    def __init__(self, r=None, g=None, b=None):
        def color():
            return random.randint(0,255)
        self.r = color() if r is None else r
        self.g = color() if g is None else g
        self.b = color() if b is None else b
    def set(self, r=None,g=None,b=None):
        if r is not None:
            self.r = r
        if g is not None:
            self.g = g
        if b is not None:
            self.b = b
    def get(self):
        return (self.r, self.g, self.b)
wall = Color(0, 128, 255).get()
floor = Color(128, 255, 255).get()
hatch = Color(255, 128, 0).get()
other = Color(128, 128, 192).get()


