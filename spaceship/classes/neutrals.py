from random import randint, choice
from collections import namedtuple
from typing import Tuple

from ..tools import distance
from .color import Color
from .item import Armor, Weapon, Item, items
from .charmap import item_chars, unit_chars
from .unit import Unit

class Villager(Unit):
    def __init__(self, x, y, ch="@", fg=Color.white, bg=Color.black, 
                 race="human", job="villager"):
        super().__init__(x, y, ch=ch, fg=fg, bg=bg, race=race)
        self.job = job
        
    def talk(self):
        return "{}: Are you from around here?".format(self.__class__.__name__)

    def acts(self, player, tiles, units):
        # Villagers just wander around
        def build_sight_map():
            sight_map[self.sight][self.sight] = self.character
            for (x, y) in tiles:
                if player.position == (x, y):
                    char = "@"
                    spotted = True
                elif (x, y) in units.keys():
                    char = units[(x, y)].character
                else:
                    char = tiles[(x, y)].char
            
            dx, dy = self.x - x + self.sight, self.y - y + self.sight
            sight_map[dy][dx] = char
        print(self.__class__.__name__)
        sight_range = self.sight * 2 + 1 # accounts for radius
        sight_map = [[" " for x in range(sight_range)] for y in range(sight_range)]
        build_sight_map()
        self.wander(tiles, sight_map)
    
    def wander(self, tiles, sight):
        print('wandering about')
        # filter out all tiles that are not empty spaces
        # do not want to go to tiles containing blockable objects or units
        # so filter twice: once to get floor tiles, again to get empty ones

        # these are all the non wall tiles
        points = list(filter(lambda t: tiles[t].char != "#", tiles.keys()))
        # these are all floor tiles without units on them
        emptys = list(filter(lambda xy: sight[self.y-xy[1]+self.sight][self.x-xy[0]+self.sight] not in unit_chars, points))
        point = choice(emptys)
        self.moving_torwards(point)

    def moving_torwards(self, point):
        dx = point[0] - self.x
        dy = point[1] - self.y
        dt = distance(*self.position, *point)
        x = int(round(dx / dt))
        y = int(round(dy / dt))
        self.move(x, y)

class Shopkeeper(Unit):
    def __init__(self, x, y, ch="@", fg=Color.white, bg=Color.black, 
                 race="human", job="shopkeeper"):
        super().__init__(x, y, ch=ch, fg=fg, bg=bg, race=race)
        self.job = job
        
    def talk(self):
        return "{}: Looking for something?".format(self.__class__.__name__)

class Blacksmith(Unit):
    def __init__(self, x, y, ch="@", fg=Color.white, bg=Color.black,
                race="human", job="blacksmith"):
        super().__init__(x, y, ch=ch, fg=fg, bg=bg, race=race)
        self.job = job

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

    def act(self):
        pass