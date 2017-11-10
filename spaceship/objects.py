import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))+'/../')
from PIL import Image
from namedlist import namedlist
from collections import namedtuple
from random import randint, choice, shuffle
from spaceship.color import Color
from spaceship.maps import hextup, hexone, output, blender, gradient, evaluate_blocks
from spaceship.setup_game import toInt
from spaceship.charmap import DungeonCharmap as dcm
from spaceship.charmap import WildernessCharmap as wcm
from spaceship.world import World
from player import Unit
from spaceship.tools import scroll
# TODO: Maybe move map to a new file called map and create a camera class?

'''Object holds all prototype objects used in the game until they are fully fleshed out
and are needed to be moved to their own respective files.
'''
debug = False
'''
Single Object
Engine
    Map
        World
            World Functions
        Dungeon
            Dungeon Functions
        Map functions
    Player (Entity)
    Component functions
'''

class Slot:
    def __init__(self, current=None):
        self._slot = current

    @property
    def slot(self):
        return self._slot

    @slot.setter
    def slot(self, item):
        self._slot = item
        if debug:
            print("set slot to {}".format(item))

class Inventory:
    """This is what you'll be holding -- may change this to equipped class name"""
    def __init__(self, n):
        self._inventory = [Slot() for _ in range(n)]

    def __getitem__(self, n):
        try:
            return self._inventory[n]
        except:
            IndexError("Not a valid slot number")
    
    def __setitem__(self, n, i):
        try:
            self._inventory[n].slot=i
        except:
            IndexError("Not a valid slot number")

class Backpack:
    """This is what your inventory will hold -- may change this to inventory class name"""
    def __init__(self, m=15):
        self._max = m
        self._inventory = []

    def full(self):
        return len(self._inventory) == self._max

    def add_item(self, i):
        if not self.full():
            self._inventory.append(i)

    def dump(self):
        return "\n".join(["{}. {}".format(chr(ord('a')+letter), item.name) 
            for item, letter in zip(self._inventory, range(len(self._inventory)))])