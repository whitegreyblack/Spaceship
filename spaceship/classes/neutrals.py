from typing import Tuple
from .world import World
from .item import Armor, Weapon, Item, items
from .unit import Unit
from random import randint

class Shopkeeper(Unit):
    def __init__(self, x, y, race, job, char, color):
        super().__init__(x, y, race, job, char, color)
        self.moveable = False
        
    def talk(self):
        return "{}: What you looking for?".format(self.__class__.__name__)

class Innkeeper(Unit):
    def __init__(self, x, y, race, job, char, color):
        super().__init__(x, y, race, job, char, color)
        self.movable = False

    def talk(self):
        return "{}: Need a room to stay?".format(self.__class__.__name__)

class Bishop(Unit):
    def __init__(self, x, y, race, job, char, color):
        super().__init__(x, y, race, job, char, color)

    def talk(self):
        return "{}: Blessings. Need some healing?".format(self.__class__.__name__)

    def act(self):
        print('act')
    # def do_ai_stuff(self, units, items):
    #     '''Create a decision tree where healing is priority'''
    #     for u, x, y in units:
    #         print("UNIT: ", u, x, y)
        
    #     for i, x, y in items:
    #         for ii in i:
    #             print("ITEM: ", ii, x, y)

class Soldier(Unit):
    def __init__(self, x, y, race, job, char, color):
        super().__init__(x, y, race, job, char, color)

    def talk(self):
        return "{}: Don't be causing trouble. Move along.".format(self.__class__.__name__)