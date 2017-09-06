"""Basically a file holding all possible human type npcs located in towns and taverns"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))+'/../')
from spaceship.objects import Object
from collections import namedtuple

being = namedtuple("Being", "name x y i c")

class Being(Object):
    def __init__(self, name, x, y, i, c):
        super().__init__(x, y, i ,c)
        self.name = name
        
    def __repr__(self):
        return f'[ Being ] {self.name}: ({self.x}, {self.y}, {self.i}, {self.c})'

class Human(Being):
    race = "Human"
    
    def __init__(self, name, x, y, i, c):
        super().__init__(name, x, y, i, c)

class NonHuman(Being):
    race = "NonHuman"

    def __init__(self, name):
        super().__init__(name)

if __name__ == "__main__":
    a = Being("R2 D2", 0, 0, 0, 0)
    print(a)