# position.py

"""Position component"""

from component import Component

class Position(Component):
    __slots__ = ['x', 'y']
    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y

if __name__ == "__main__":
    from util import dprint, gso
    p = Position(0, 0)
    print(p, repr(p), dprint(p), gso(p))

