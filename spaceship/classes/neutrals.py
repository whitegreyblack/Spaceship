from random import randint, choice
from collections import namedtuple
from typing import Tuple

from ..tools import distance
from .color import Color
from .item import Armor, Weapon, Item, items
from .charmap import item_chars, unit_chars
from .unit import Unit

class VillagerChild(Unit):
    def __init__(self, x, y, ch="v", fg=Color.white, bg=Color.black, 
                 race="human", job="villager", rs=0):
        super().__init__(x, y, ch=ch, fg=fg, bg=bg, race=race, rs=rs)
        self.job = job
        
    def talk(self):
        return "{}: Are you from around here?".format(self.__class__.__name__)

    def acts(self, player, tiles, units):
        # Villagers just wander around
        def build_sight_map():
            def map_out():
                return "\n".join("".join(row[::-1]) for row in sight_map[::-1])

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
            sight_map[self.sight][self.sight] = self.character

            print(map_out())
        sight_range = self.sight * 2 + 1 # accounts for radius
        sight_map = [[" " for x in range(sight_range)] for y in range(sight_range)]
        build_sight_map()
        self.wander(tiles, sight_map)
    
    def wander(self, tiles, sight):
        def within(x, y):
            return 6 <= x <= 60 and 2 <= y <= 20
        points = list(filter(lambda t: within(*t) and not tiles[t].block_mov, tiles.keys()))
        emptys = list(filter(lambda xy: sight[self.y-xy[1]+self.sight][self.x-xy[0]+self.sight] not in unit_chars, points))
        point = choice(emptys)
        print(tiles[point].char, tiles[point].block_mov)
        self.moving_torwards(point)

    def moving_torwards(self, point):
        dx = point[0] - self.x
        dy = point[1] - self.y
        dt = distance(*self.position, *point)
        x = int(round(dx / dt))
        y = int(round(dy / dt))
        self.move(x, y)

class Villager(Unit):
    def __init__(self, x, y, ch="V", fg=Color.white, bg=Color.black, 
                 race="human", job="villager", rs=0):
        super().__init__(x, y, ch=ch, fg=fg, bg=bg, race=race, rs=rs)
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
        sight_range = self.sight * 2 + 1 # accounts for radius
        sight_map = [[" " for x in range(sight_range)] for y in range(sight_range)]
        build_sight_map()
        self.wander(tiles, sight_map)
    
    def wander(self, tiles, sight):
        points = list(filter(lambda t: tiles[t].char != "#", tiles.keys()))
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
    def __init__(self, x, y, ch="S", fg=Color.white, bg=Color.black, 
                 race="human", job="shopkeeper", rs=0):
        super().__init__(x, y, ch=ch, fg=fg, bg=bg, race=race, rs=rs)
        self.job = job
        
    def talk(self):
        return "{}: Looking for something?".format(self.__class__.__name__)

class Blacksmith(Unit):
    def __init__(self, x, y, ch="B", fg=Color.white, bg=Color.black,
                race="human", job="blacksmith", rs=0):
        super().__init__(x, y, ch=ch, fg=fg, bg=bg, race=race, rs=rs)
        self.job = job

class Innkeeper(Unit):
    def __init__(self, x, y, ch="I", fg=Color.white, bg=Color.black, 
                 race="human", job="innkeeper", rs=0):        
        super().__init__(x, y, ch=ch, fg=fg, bg=bg, race=race, rs=rs)
        self.job = job
        self.moveable = False

    def talk(self):
        return "{}: Need a room to stay?".format(self.__class__.__name__)

class Bishop(Unit):
    def __init__(self, x, y, ch="B", fg=Color.white, bg=Color.black, 
                 race="human", job="bishop", rs=0):        
        super().__init__(x, y, ch=ch, fg=fg, bg=bg, race=race, rs=rs)
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

class Soldier(Unit):
    ''' soldier class should be on patrol -- moves from position to position
    IF an enemy is spotted then chase
    if an enemy dies or runs too far away then patrol again
    soldier class can also go on standmode which makes them stand still
    this also makes it so that soldier ar not displaceable by player
    or other units
    '''
    def __init__(self, x, y, ch="G", fg=Color.white, bg=Color.black, 
                 race="human", job="soldierr", rs=0):        
        super().__init__(x, y, ch=ch, fg=fg, bg=bg, race=race, rs=rs)
        self.job = job
        
    def talk(self):
        return "{}: Don't be causing trouble. Move along.".format(self.__class__.__name__)

    def act(self):
        pass