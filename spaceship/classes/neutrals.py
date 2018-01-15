from random import randint, choice
from collections import namedtuple
from typing import Tuple

from ..tools import distance
from .color import Color
from .item import Armor, Weapon, Item, items, item_chars
from .unit import Unit, unit_chars

class VillagerChild(Unit):
    def __init__(self, x, y, ch="v", fg=Color.white, bg=Color.black, 
                 race="human", job="villager", rs=0):
        super().__init__(x, y, ch=ch, fg=fg, bg=bg, race=race, rs=rs)
        self.sight = self.sight_city
        self.job = job
        self.spaces = spaces 
    
    def talk(self):
        return "{}: Are you from around here?".format(self.__class__.__name__)

    def acts(self, units, tiles):
        # Villagers just wander around
        def build_sight_map():
            for (x, y) in tiles:
                if player.position == (x, y):
                    char = "@"
                    spotted = True

                elif (x, y) in units.keys():
                    char = units[(x, y)].character

                else:
                    char = tiles[(x, y)].char
            
                dx, dy = self.translate_sight(x, y)

                sight_map[dy][dx] = char

            sight_map[self.sight][self.sight] = self.character

        sight_range = self.sight * 2 + 1 # accounts for radius
        sight_map = [[" " 
            for x in range(sight_range)] 
            for y in range(sight_range)]
            
        build_sight_map()
        self.wander(tiles, sight_map)
    
    def wander(self, tiles, sight):

        def translate(x, y):
            sx, sy = self.translate_sight(x, y)
            return sight[sy][sx] not in unit_chars

        # points = list(filter(lambda t: within(*t) and not tiles[t].block_mov, 
        #                       tiles.keys()))
        points = list(filter(
            lambda t: self.within(*t) and not tiles[(x, y)].block_mov, 
            tiles.keys()))

        # emptys = list(filter(lambda xy: 
        #   sight[self.y - xy[1] + self.sight][self.x - xy[0] + self.sight] 
        #       not in unit_chars, 
        #   points))
        emptys = list(filter(lambda xy: translate(*xy), points))
        point = choice(emptys)
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
                 race="human", job="villager", rs=0, spaces=[]):
        super().__init__(x, y, ch=ch, fg=fg, bg=bg, race=race, rs=rs)
        self.job = job
        self.spaces = spaces 
        self.sight = self.sight_city

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
                 race="human", job="shopkeeper", rs=0, spaces=[]):
        super().__init__(x, y, ch=ch, fg=fg, bg=bg, race=race, rs=rs)
        self.job = job
        self.spaces = spaces 
        self.sight = self.sight_city

    def talk(self):
        return "{}: Looking for something?".format(self.__class__.__name__)

    def acts(self, player, tiles, units):
        spaces = list(filter(lambda xy: xy != self.position, self.spaces))
        self.moving_torwards(choice(spaces))

    def moving_torwards(self, point):
        dx = point[0] - self.x
        dy = point[1] - self.y
        dt = distance(*self.position, *point)
        x = int(round(dx / dt))
        y = int(round(dy / dt))
        self.move(x, y)        

class Blacksmith(Unit):
    def __init__(self, x, y, ch="B", fg=Color.white, bg=Color.black,
                race="human", job="blacksmith", rs=0, spaces=[]):
        super().__init__(x, y, ch=ch, fg=fg, bg=bg, race=race, rs=rs)
        self.job = job
        self.spaces = spaces 
        self.sight = self.sight_city

class Innkeeper(Unit):
    def __init__(self, x, y, ch="I", fg=Color.white, bg=Color.black, 
                 race="human", job="innkeeper", rs=0, spaces=[]):        
        super().__init__(x, y, ch=ch, fg=fg, bg=bg, race=race, rs=rs)
        self.job = job
        self.spaces = spaces
        self.sight = self.sight_city

    def talk(self):
        return "{}: Need a room to stay?".format(self.__class__.__name__)

    def acts(self, player, tiles, units):
        spaces = list(filter(lambda xy: xy != self.position, self.spaces))
        self.moving_torwards(choice(spaces))

    def moving_torwards(self, point):
        dx = point[0] - self.x
        dy = point[1] - self.y
        dt = distance(*self.position, *point)
        x = int(round(dx / dt))
        y = int(round(dy / dt))
        self.move(x, y)        

class Bishop(Unit):
    def __init__(self, x, y, ch="B", fg=Color.white, bg=Color.black, 
                 race="human", job="bishop", rs=0, spaces=[]):        
        super().__init__(x, y, ch=ch, fg=fg, bg=bg, race=race, rs=rs)
        self.job = job
        self.spaces = spaces
        self.sight = self.sight_city

    def talk(self):
        return "{}: Blessings. Need some healing?".format(self.__class__.__name__)
    
    def acts(self, player, tiles, units):
        spaces = list(filter(lambda xy: xy != self.position, self.spaces))
        self.moving_torwards(choice(spaces))

    def acts(self, units, tiles):
        def build_sight_map():
            '''purely visual recording of environment -- no evaluation yet'''
            def map_out():
                return "\n".join("".join(row[::-1]) for row in sight_map[::-1])

            sight_map[self.sight_norm][self.sight_norm] = self.character
            spotted = False

            for tile in tiles:
                if tile in units.keys():
                    # check if unit is on the square
                    unit = units[tile]
                    char = unit.character
                    spotted = True
                    if unit.behaviour_score < 0:
                        paths.append((100, unit, self.path(self.position, unit.position, tiles)))

                elif tiles[tile].items:
                    # check for items on the square
                    char = tiles[tile].items[0].char

                else:
                    # empty square
                    char = tiles[tile].char

                # offset the location based on unit position and sight range
                x, y = tile
                dx, dy = self.translate_sight(x, y)
                sight_map[dy][dx] = char

            # if spotted:
            #     print(map_out())

        paths = []            
        unit_spotted = []
        item_spotted = []

        sight_range = self.sight_norm * 2 + 1 # accounts for radius
        sight_map = [[" " for x in range(sight_range)] for y in range(sight_range)]
        build_sight_map()

        if self.cur_hp <= self.tot_hp * .10:
            return commands_ai['wait']

        else:
            if not paths:
                # nothing of interest to the bishop
                self.wander(tiles, sight_map)

            # else:
            #     print('not wander')
            #     _, interest, path = max(paths)
            #     # print(self.position, interest, path)
            #     if not path:
            #         # path returns false
            #         self.wander(tiles, sight_map)
            #     # get distance to determine action
            #     # elif isinstance(interest, Unit) or isinstance(interest, Player):
            #     elif isinstance(interest, Unit):
            #         if self.race in interest.__class__.__name__:
            #             # print('Saw another {}'.format(self.race))
            #             pass
            #         else:
            #             dt = distance(*self.position, *interest.position)
            #             if dt < 2:
            #                 # x, y = self.x - interest.x, self.y - interest.y
            #                 # self.attack(interest)
            #                 return commands_ai['move'][self.direction(interest)]

            #             else:
            #                 # print("Saw {}".format(interest))
            #                 self.follow(sight_map, units, path[1].node)

class Soldier(Unit):
    ''' soldier class should be on patrol -- moves from position to position
    IF an enemy is spotted then chase
    if an enemy dies or runs too far away then patrol again
    soldier class can also go on standmode which makes them stand still
    this also makes it so that soldier ar not displaceable by player
    or other units
    '''
    def __init__(self, x, y, ch="G", fg=Color.white, bg=Color.black, 
                 race="human", job="soldierr", rs=0, spaces=[]):        
        super().__init__(x, y, ch=ch, fg=fg, bg=bg, race=race, rs=rs)
        self.job = job
        self.spaces = spaces 
        self.sight = self.sight_city

    def talk(self):
        return "{}: Don't be causing trouble. Move along.".format(self.__class__.__name__)

    def acts(self, player, tiles, units):
        spaces = list(filter(lambda xy: xy != self.position, self.spaces))
        self.moving_torwards(choice(spaces))

    def moving_torwards(self, point):
        dx = point[0] - self.x
        dy = point[1] - self.y
        dt = distance(*self.position, *point)
        x = int(round(dx / dt))
        y = int(round(dy / dt))
        self.move(x, y)        

neutrals = {
    "bishop": Bishop,
    "innkeeper": Innkeeper,
    "shopkeeper": Shopkeeper,
    "soldier": Soldier,
    "villager": Villager,
    "blacksmith": Blacksmith,
    "child": VillagerChild,
}