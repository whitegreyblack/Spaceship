from typing import Tuple
from .color import Color
from .world import World
from .item import Armor, Weapon, Item, items
from .unit import Unit
from random import randint

class Shopkeeper(Unit):
    def __init__(self, x, y, ch="@", fg=Color.white, bg=Color.black, 
                 race="human", job="shopkeeper"):
        super().__init__(x, y, ch=ch, fg=fg, bg=bg, race=race)
        self.job = job
        
    def talk(self):
        return "{}: What you looking for?".format(self.__class__.__name__)

class Innkeeper(Unit):
    def __init__(self, x, y, ch="@", fg=Color.white, bg=Color.black, 
                 race="human", job="innkeeper"):        
        super().__init__(x, y, ch=ch, fg=fg, bg=bg, race=race)
        self.job = job
        self.moveable = False

    def talk(self):
        return "{}: Need a room to stay?".format(self.__class__.__name__)

class Bishop(Unit):
    def __init__(self, x, y, ch="@", fg=Color.white, bg=Color.black, 
                 race="human", job="bishop"):        
        super().__init__(x, y, ch=ch, fg=fg, bg=bg, race=race)
        self.job = job
        
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

# soldier class should be on patrol -- moves from position to position
# IF an enemy is spotted then chase
# if an enemy dies or runs too far away then patrol again
# soldier class can also go on standmode which makes them stand still
# this also makes it so that soldier ar not displaceable by player
# or other units
class Soldier(Unit):
    def __init__(self, x, y, ch="@", fg=Color.white, bg=Color.black, 
                 race="human", job="soldierr"):        
        super().__init__(x, y, ch=ch, fg=fg, bg=bg, race=race)
        self.job = job
        
    def talk(self):
        return "{}: Don't be causing trouble. Move along.".format(self.__class__.__name__)