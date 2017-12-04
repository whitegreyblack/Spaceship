 # -*- coding=utf-8 -*-
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))+'/../../')
from bearlibterminal import terminal as term
from PIL import Image, ImageDraw
from functools import lru_cache
from random import randint, choice, shuffle
from spaceship.tools import bresenhams
from math import hypot
from copy import deepcopy
from textwrap import wrap
from namedlist import namedlist
from collections import namedtuple
from spaceship.maps.charmap import DungeonCharmap as dcm
from spaceship.maps.charmap import WildernessCharmap as wcm
from spaceship.tools import scroll
from spaceship.units.monsters import Rat, Bat

'''
TODO: seperate map and dungeon
Map holds:
    dungeon class
    list of items
    list of units
    list of sight
    list of maps(dungeons) below it 
World holds:
    list of maps basically a connected linked list?'

For example
    Overworld 8x8 64 tiles
    Assume half is water so 32 tiles are land 
    Each land tile will hold an overworld map
    for each city in city/village list:
        draw a city tile on the map
        read in the city map from the string file
        these tiles will not be considered land tiles anymore
    there will also be a list of pyramid dungeons throughout the map which will have their own list of 
        dungeons
        these tiles will also not be considered land tiles
    For each land tile that is not a mountain:
        it has a chance to hold a dungeon i guess
'''

class Map:
    class Tile:
        def __init__(self, char, color, block_mov, block_lit):
            self.char = char
            self.color = color
            self.block_mov = block_mov
            self.block_lit = block_lit
            self.items = []
            self.light = 0

    mult = [
                [1,  0,  0, -1, -1,  0,  0,  1],
                [0,  1, -1,  0,  0, -1,  1,  0],
                [0,  1,  1,  0,  0, -1, -1,  0],
                [1,  0,  0,  1, -1,  0,  0, -1]
            ]

    # tile = namedlist("Tile", "char color bkgd light block_mov block_lit items")
    chars_block_move = {"#", "+", "o", "x", "~", "%", "Y", "T"}
    chars_block_light = {"#", "+", "o", "%", "Y", "T"}

    def __init__(self, width, height, map_type):
        self.map_type = map_type
        # terminal viewing dimensions
        if not hasattr(self, 'width'):
            self.width = 66
        if not hasattr(self, 'height'):
            self.height = 22
        # self.width, self.height = 66, 22
        self.map_display_width = min(66, width)
        self.map_display_height = min(22, height)
        self.units = []

    def build(self):
        raise NotImplementedError("cannot build the base map class -- use a child map object")

    def __str__(self):
        return "\n".join("".join(row) for row in self.data)

    def __repr__(self):
        return "{}: ({}, {})".format(self.__class__.__name__, self.width, self.height)

    def debug_set_global_light(self):
        for y in range(self.height):
            for x in range(self.width):
                self.square(x, y).light = 2
                
    ###########################################################################
    # Level Initialization, Setup, Terraform and Evaluation                   #
    ###########################################################################
    def dimensions(self):
        '''takes in a string map and returns a 2D list map and map dimensions'''
        if hasattr(self, 'data'):
            self.height = len(self.data)
            self.width = max(len(col) for col in self.data)
        else:
            raise AttributeError("No self.data")

    def create_tile_map(self):
        if not hasattr(self, 'data'):
            raise AttributeError("No self.data")
        if not hasattr(self, 'chars'):
            raise AttributeError("No self.chars")

        rows = []   
        for row in self.data:
            cols = []
            for char in row:
                try:
                    chars, hexcodes = self.chars[char]
                except KeyError:
                    raise KeyError("Evaluate Map: {} not in keys".format(char))

                block_mov = char in self.chars_block_move
                block_lit = char not in self.chars_block_light

                tile = self.Tile(
                    char=choice(chars),
                    color=choice(hexcodes),
                    block_mov=block_mov,
                    block_lit=block_lit)

                cols.append(tile)
            rows.append(cols)
        self.tilemap = rows        

    def check_data(self):
        if hasattr(self, 'data'):
            return True
        else:
            raise AttributeError("No self.data")
    
    def check_chars(self):
        if hasattr(self, 'chars'):
            return True
        else:
            raise AttributeError("No self.chars")
    
    def check_exists(self, attrs):
        for attr in attrs:
            if not hasattr(self, attr):
                raise AttributeError("No self.{}".format(attr))
        return True
    ###########################################################################
    # Connected Map/Dungeon Functions and Properties                          #
    ###########################################################################
    def getUpStairs(self):
        '''find exit and save on the first time
        subsequent calls returns the saved point'''
        if hasattr(self, "exitpoint"):
            return self.exitpoint

        for j in range(len(self.data)):
            for i in range(len(self.data[0])):
                if self.data[j][i] == "<":
                    self.exitpoint = i, j
                    return i, j

    def getDownStairs(self):
        '''same logic as getExit'''
        try:
            if hasattr(self, self.enterance):
                return self.enterance
        except AttributeError:
            # manually look through the map to check for '>'
            for j in range(len(self.data)):
                for i in range(len(self.data[0])):
                    if self.data[j][i] == ">":
                        self.entrance = i, j
                        return i, j
            return 'Doesnt have a sublevel?'

    def hasParent(self, parent):
        return hasattr(self, 'parent')

    def addParent(self, parent):
        self.parent = parent

    def getParent(self):
        return self.parent

    def hasSublevel(self):
        return hasattr(self, 'sublevel')

    def addSublevel(self, sublevel):
        self.sublevel = sublevel

    def getSublevel(self):
        return self.sublevel

    ###########################################################################
    #  Singular Map Functions                                                 #
    ###########################################################################
    def square(self, x, y):
        # return self.data[y][x]
        return self.tilemap[y][x]

    def within_bounds(self, x, y):
        return 0 <= x < self.width and 0 <= y < self.height

    def out_of_bounds(self, x, y):
        return not self.within_bounds(x, y)

    def walkable(self, x, y):
        '''Checks for bounds of map and blockable tile objects'''
        return self.within_bounds(x, y) and not self.square(x, y).block_mov

    def viewable(self, x, y):
        '''Only acts on objects within the bounds of the map'''
        return self.within_bounds(x, y) and self.square(x, y).block_lit

    def occupied(self, x, y):
        '''Only acts on unit objects in the map'''
        return self.within_bounds(x, y) and (x, y) in self.get_unit_positions()

    def blocked(self, x, y):
        '''Only acts on objects within the bounds of the map'''
        return self.out_of_bounds(x, y) or self.square(x, y).block_mov

    def open_door(self, x, y):
        def is_closed_door(x, y):
            return self.square(x,y).char == "+"
        if is_closed_door(x, y):
            self.square(x, y).char = "/"

    def close_door(self, x, y):
        def is_opened_door(x, y):
            return self.square(x, y).char == "/"
        if is_opened_door(x, y):
            self.square(x, y).char = "+"

    def reblock(self, x, y):
        self.square(x, y).block_mov = True

    def unblock(self, x, y):
        self.square(x, y).block_mov = False
    ###########################################################################
    # Sight, Light and Color Functions                                        #
    ###########################################################################
    def check_light_level(self, x, y):
        return self.square(x, y).light

    def set_light_level(self, x, y, v):
        if self.within_bounds(x, y):
            self.square(x, y).light = v

    def lit_reset(self):
        for y in range(self.height):
            for x in range(self.width):
                if self.square(x, y).light == 2:
                    self.square(x, y).light = 1 # if self.square(x, y).light > 0 else 0

    def fov_calc_blocks(self, x, y, r, player):
        def fov_block(cx, cy, row, start, end, radius, xx, xy, yx, yy, id):
            nonlocal vision_tiles
            if start < end:
                return

            radius_squared = radius * radius

            for j in range(row, radius + 1):
                dx, dy = -j - 1, -j
                blocked = False

                while dx <= 0:
                    dx += 1
                    X, Y = cx + dx * xx + dy * xy, cy + dx * yx + dy * yy
                    l_slope, r_slope = (dx - 0.5) / (dy + 0.5), (dx + 0.5) / (dy-0.5)
                    
                    if start < r_slope:
                        continue
                    
                    elif end > l_slope:
                        break
                    
                    else:
                        if dx * dx + dy * dy < radius_squared:
                            if self.within_bounds(X, Y):
                                vision_tiles.add((X, Y))
                            # self.set_light_level(X, Y, 2)
                        if blocked:
                            if self.blocked(X, Y) and not self.viewable(X, Y):
                                new_start = r_slope
                                
                            else:
                                blocked = False
                                start = new_start
                        else:
                            if self.blocked(X, Y) and not self.viewable(X, Y) and j < radius:
                                blocked = True
                                self.sight(cx, cy, j + 1, start, l_slope,
                                            radius, xx, xy, yx, yy, id + 1)
                                new_start = r_slope
                if blocked:
                    break

        def split_blocks():
            '''Returns "interesting details from the map positions in
            the line of sight of unit
            '''
            nonlocal vision_tiles
            # get units
            units = {}
            items = []
            for x, y in vision_tiles:
                if (x, y) == player.position_local():
                    units[(x, y)] = player
            return units, items

        vision_tiles = set()
        for o in range(8):
            fov_block(x, y, 1, 1.0, 0.0, r,
                        self.mult[0][o], 
                        self.mult[1][o], 
                        self.mult[2][o], 
                        self.mult[3][o], 0)
        # return split_blocks()
        return vision_tiles

    def fov_calc(self, unit):
        for x, y, radius in unit:
            for o in range(8):
                self.sight(x, y, 1, 1.0, 0.0, radius,
                        self.mult[0][o], 
                        self.mult[1][o], 
                        self.mult[2][o], 
                        self.mult[3][o], 0)

    def sight(self, cx, cy, row, start, end, radius, xx, xy, yx, yy, id):
        if start < end:
            return

        radius_squared = radius * radius

        for j in range(row, radius + 1):

            dx, dy = -j - 1, -j
            blocked = False

            while dx <= 0:
                dx += 1
                X, Y = cx + dx * xx + dy * xy, cy + dx * yx + dy * yy
                # l_slope and r_slope store the slopes of the left and right
                # extremities of the square we're considering:
                l_slope, r_slope = (dx - 0.5) / (dy + 0.5), (dx + 0.5) / (dy - 0.5)
                if start < r_slope:
                    continue

                elif end > l_slope:
                    break

                else:
                    # Our light beam is touching this square; light it:
                    if dx * dx + dy * dy < radius_squared:
                        self.set_light_level(X, Y, 2)

                    if blocked:
                        # we're scanning a row of blocked squares:
                        # if self.blocked and self.viewable         - window
                        # if self.blocked and not self.viewable     - wall
                        # if not self.blocked and self.viewable     - floor
                        # if not self.blocked and not self.viewable - empty space
                        if self.blocked(X, Y) and not self.viewable(X, Y):
                            new_start = r_slope
                        # elif self.blocked(X, Y) and self.viewable(X, Y):
                        #     blocked = False
                        #     start = new_start
                        # if not self.blocked(x, y)
                        else:
                            blocked = False
                            start = new_start
                    else:
                        if self.blocked(X, Y) and not self.viewable(X, Y) and j < radius:
                            # This is a blocking square, start a child scan:
                            blocked = True
                            self.sight(cx, cy, j + 1, start, l_slope,
                                        radius, xx, xy, yx, yy, id + 1)
                            new_start = r_slope

            # Row is scanned; do next row unless last square was blocked:
            if blocked:
                break
            
    ###########################################################################
    # Item object Functions                                                   #
    ###########################################################################
    def add_item(self, x, y, i):
        self.square(x, y).items.append(i)

    def get_item(self, x, y):
        return self.square(x, y).items
    ###########################################################################
    # Unit object Functions                                                   #
    ###########################################################################
    def unit_at(self, x, y):
        return self.square(x, y).unit

    def get_unit(self, x, y):
        '''Returns units by positional values'''
        if hasattr(self, 'units'):
            for u in self.units:
                if (x, y) == u.position():
                    return u
        return []

    def get_units(self):
        '''Returns all units within the list'''
        if hasattr(self, 'units'):
            for unit in self.units:
                yield unit
        return []

    def get_unit_positions(self):
        if hasattr(self, 'units'):
            return {u.position() for u in self.units}
        return {}

    def remove_unit(self, unit):
        if hasattr(self, 'units'):
            self.units.remove(unit)

    def process_unit_actions(self, player):
        for unit in self.units:
            if hasattr(unit, 'do_ai_stuff'):
                units, items = self.fov_calc_blocks(unit.x, unit.y, unit.sight)
                unit.do_ai_stuff(units, items)

    def handle_units(self, player):
        # print(hasattr(self, 'units'))
        for unit in self.units:
            print(unit)
            if hasattr(unit, 'acts'):
                units, items = [], []
                tiles = self.fov_calc_blocks(unit.x, unit.y, unit.sight, player)
                for x, y in tiles:
                    if (x, y) == player.position_local():
                        units.append(player)
                    # elif self.square(x, y).unit:
                    #     units.append(self.square(x, y).unit)
                    if self.square(x, y).items:
                        items.append(self.square(x, y).items)
                unit.acts(player, units, items)
                    # elif self.square(x, y).unit:

    def generate_units(self):
        if self.height <= 25:
            max_units = 1
        else:
            max_units = 2

        if hasattr(self, 'spaces'):
            shuffle(self.spaces)
            for i in range(max_units):
                i, j = self.spaces[randint(0, len(self.spaces)-1)]
                unit = choice([Rat, Rat])(x=i, y=j)
                self.units.append(unit)
                self.square(i, j).unit = unit
        else:
            raise AttributeError("Spaces has not yet been initialized")

    def reduce_unit_relationships(self, reduce):
        self.relationship = min(-100, max(self.relationship - reduce, 100))

    def increase_unit_relationships(self, increase):
        self.relationship = min(-100, max(self.relationship - increase, 100))
        return "Your relationship with {} has decreased by {}".format(self.map_id)

    ###########################################################################
    # Output and Display Functions                                            #
    ###########################################################################
    def output(self, player_x, player_y):
        shorten_x = self.map_display_width > 66
        shorten_y = self.map_display_height > 44

        # get camera location for x coordinate
        cam_x = scroll(
            player_x, 
            self.map_display_width + (-14 if shorten_x else 0), 
            self.width)
        ext_x = cam_x + self.map_display_width + (-14 if shorten_x else 0)
        
        # get camera location for y coordinate
        cam_y = scroll(
            player_y, 
            self.map_display_height + (-6 if shorten_y else 0), 
            self.height)
        ext_y = cam_y + self.map_display_height + (-6 if shorten_y else 0)

        positions = {}
        if hasattr(self, 'units') and self.units:
            for unit in self.units:
                positions[unit.position()] = unit

        col = "#ffffff"
        # width should total 80 units
        for x in range(cam_x, ext_x):

            # height should total 24 units
            for y in range(cam_y, ext_y):
                # reset variables every iteration
                if x == player_x and y == player_y:
                    # Current position holds your position
                    ch = "@"
                    col = "white"

                elif (x, y) in positions.keys():
                    # Current position holds a unit
                    lit = self.check_light_level(x, y)
                    if lit == 2:
                        ch = positions[(x, y)].character
                        col = positions[(x, y)].color
                    elif lit == 1:
                        ch, col = self.square(x, y).char, 'darkest grey'
                    else:
                        ch, col = " ", "black"


                # Current position holds an item
                elif self.square(x, y).items:
                    if self.check_light_level(x, y) == 2:
                        item = self.square(x, y).items[0]
                        ch = item.char
                        col = item.color
                    else:
                        ch = self.square(x, y).char
                        col = "darkest grey"

                # Current position holds a Lamp
                    # elif (x, y, 10) in self.lamps:
                    #     level = ""
                    #     ch = self.square(x, y).char
                    #     col = "white"

                # deal with displaying traps
                    # elif self.square(x, y).char == '^':
                    #     lit = self.lit(x, y)
                    #     if lit:
                    #         if lit == 2:
                    #             ch = self.square(x, y).char
                    #             col = self.square(x, y).color
                    #         else:
                    #             ch = self.square(x, y).char
                    #             col = Color.color('grey darkest')
                    #     else:
                    #         ch, col, bkgd = ".", "black", None

                else:
                    # all other environment features
                    lit = self.check_light_level(x, y)
                    if lit == 2:
                        ch = self.square(x, y).char
                        col = self.square(x, y).color
                    elif lit == 1:
                        ch = self.square(x, y).char
                        col = "darkest grey"
                    else:
                        ch, col = " ", "black"
                yield (x - cam_x, y - cam_y, col, ch)

        # print(self.tilemap[10][10])
        self.lit_reset()

# TEST: blender function
# if __name__ == "__main__":
#     if len(sys.argv) < 4:
#         print(sys.argv)
#         exit('ERROR :- incorrect num of args')
        
#     term.open()
#     term.set("window: size=80x25")
#     colors = blender(sys.argv[1], sys.argv[2], int(sys.argv[3]))
#     print(colors)
#     step = 80 // len(colors)
#     for i in range(len(colors)):
#         for y in range(25):
#             for x in range(step):
#                 term.puts(step*i+x, y, "[color={}]%[/color]".format(colors[i]))
#     term.refresh()
#     term.read()

# Test: Map class
# if __name__ == "__main__":
#     test = Map(66, 22)
#     print(test)
