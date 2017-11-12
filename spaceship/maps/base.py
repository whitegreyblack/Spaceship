 # -*- coding=utf-8 -*-
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))+'/../../')
from spaceship.action import num_movement
from bearlibterminal import terminal as term
from PIL import Image, ImageDraw
from functools import lru_cache
from random import randint, choice
from spaceship.tools import bresenhams
from math import hypot
from copy import deepcopy
from textwrap import wrap
from namedlist import namedlist
from collections import namedtuple
from spaceship.maps.charmap import DungeonCharmap as dcm
from spaceship.maps.charmap import WildernessCharmap as wcm
from spaceship.tools import scroll

"""Maps file holds template functions that return randomized data maps used\
in creating procedural worlds"""
class Light: Unexplored, Explored, Visible = range(3)    
class Letter: Ascii, Unicode = range(2)
chars_block_move= {"#", "+", "o", "x", "~", "%", "Y", "T"}
chars_block_move_hills =  {"#", "+", "o", "x", "%", "Y", "T"}
chars_block_light = {"#", "+", "o", "%", "Y", "T"}

# Key-value pairs are mapped from characters to color tuples
# used when converting maps into color images
picturfy_chars = {
    "#": (0,0,0),
    "%": (136, 0, 21),
    "o": (255, 242, 0),
    ",": (34, 177, 76),
    "+": (185, 122, 87),
    "=": (112, 146, 190),
    ".": (127, 127, 127),
    ".": (255, 255, 255),
    ":": (195, 195, 195),
    "~": (0, 162, 232),
    "|": (241, 203, 88),
    "x": (98, 81, 43),
}

# Key-Value pairs are tuples to tuple pertaining to color and character mapping
# used in converting colored images into string maps
stringify_chars = { 
    (0, 0, 0): "#",
    (136, 0, 21): "%",
    (255, 242, 0): "=",
    (34, 177, 76): ",",
    (185, 122, 87): "+",
    (127, 127, 127): ".",
    (112, 146, 190): "=",   
    (153, 217, 234): "=",
    (255, 255, 255): ".",
    (195, 195, 195): ":",
    (241, 203, 88): "|",
    (255, 201, 14): "|",
    (0, 162, 232): "~",
    (98, 81, 43): "x",
    (239, 228, 176): ",",
}

stringify_world = {
    (112, 146, 190): "=",
}

unicode_blocks_thin = {
    0: "25D9",
    1: "25D9",
    2: "25D9",
    #3: "255A",
    3: "25D9",
    4: "25D9",
    5: "2551",
    #6: "2554",
    6: "25D9",
    7: "2560",
    8: "25D9",
#   9: "255D",
    9: "25D9",
    10: "2550",
    11: "2569",
#   12: "2557",
    12: "25D9",
    13: "2562",
    14: "2566",
    15: "256C",
}

def toInt(hexval):
    try:
        return int(hexval, 16)
    except TypeError:
        print("TOINT ERROR:", hexval)
        raise

def picturfy(string, filename="picturfy-img.png", folder="./", debug=False):
    """Takes in a list of string lists and three positional parameters.
    Filename and folder are used to determine the output path after 
    function execution. Debug is used to print testing and terminal
    output. The inverse function to stringify and asciify"""

    mapping = string.split('\n')
    h, w = len(mapping), len(mapping[0])
    img_to_save = Image.new('RGB', (w, h))
    drawer = ImageDraw.Draw(img_to_save)

    for j in range(h):
        string_list = list(mapping[j])
        for i in range(len(string_list)):
            drawer.rectangle((i, j, i+1, j+1), picturfy_chars[string_list[i]])

    print("Saving string as {}".format(folder+filename))
    img_to_save.save(folder+filename)
    return folder+filename

def asciify(string, debug=False):
    """Takes in a file location string and a debug parameter
    to determine output. Sister function to stringify. Uses
    unicode characters provided they are available in blt."""
    array = []
    colors = set()
    with Image.open(string) as img:
        pixels = img.load()
        w, h = img.size
    
    # first pass -- evaluates and transforms colors into string characters
    # second pass -- evaluates and transforms ascii characters into unicode
    for j in range(h):
        column = []
        for i in range(w):
            try:
                r, g, b, _ = pixels[i, j]
            except ValueError:
                r, g, b = pixels[i, j]
            if (r, g, b) not in colors:
                colors.add((r,g,b))
            try:
                column.append(stringify_chars[(r, g, b)])
            except KeyError:
                print((r, g, b))
        array.append(column)

    if debug:
        for i in range(h):
            print("".join(array[i]))
        print(colors)

    # return evaluate_block(lines, w, h)

    # returns a 2D array/map
    return array

def evaluate_blocks(data, w, h, array=False):
    """Helper function for asciify which returns the same sized map
    but with the indices holding unicode character codes"""
    def evalValue(x, y):
        bit_value=0
        increment=1
        debug=11
        for i, j in ((0,-1), (1,0), (0,1), (-1, 0)):
                try:
                    char = data[y+j][x+i]
                except IndexError:
                    char = ""
                if char in ("#", "o", "+"):
                    bit_value += increment
                increment *= 2
        return bit_value

    unicodes = deepcopy(data)
    for i in range(h):
        for j in range(w):
            if data[i][j] == "#":
                unicodes[i][j] = toInt(unicode_blocks_thin[evalValue(j, i)])
    return unicodes

def table(ch, val, x, y):
    """Returns a 2d list of lists holding a four element tuple"""
    return [[(choice(ch), choice(val), i, j) for i in range(x)] for j in range(y)]

def splitter(c):
    c = c.replace("#", "")
    if len(c) >= 8:
        c = c[2::]
    return wrap(c,2)

def darken(hexcode):
    return

def blender(hexes, n=10):
    """blender holds color transformation functions
    TODO: probably should move this to another file
    Up to user to decide whether color is valid"""
    hex1, hex2 = hexes
    
    def transform(c):
        # for i in c:
        #   integer = int(i, 16)
        return [int(i, 16) for i in c]

    def blend(ca, cb, n, i):
        value = ca - cb
        value /= n
        value *= i
        value = round(value)
        value = hex(cb+value)
        value = value.replace("0x", "")
        #value = hex(((abs(ca-cb)//n))*i).replace("0x", "")
        return value

    def mash(color):
        return "#ff"+"".join(map(lambda x: "0"+str(x) if len(str(x)) < 2 else str(x), color))

    colorA = transform(splitter(hex2))
    colorB = transform(splitter(hex1))
    colorS = [mash(splitter(hex1.replace("#","")))]

    for i in range(n-2):
        color=[]
        for j in range(3):
            color.append(blend(colorA[j], colorB[j], n-2, i))
        colorS.append(mash(color))

    colorS.append(mash(splitter(hex2.replace("#",""))))
    
    return colorS

def hexify(x):
    """Returns a single hex transformed value as a string"""
    return hex(x).split('x')[1] if x > 15 else '0' + hex(x).split('x')[1]


def hextup(x, a, b, c):
    """Returns a triple hex valued tuple as ARGB hex string"""
    return "#ff" \
        + hexify(x//a) \
        + hexify(x//b) \
        + hexify(x//c)


def hexone(x):
    return "#ff" + hexify(x) * 3


def output(data):
    lines = []
    characters = {}

    for row in data:
        line = ""
        for c, _, _, _ in row:
            try:
                characters[c] += 1
            except KeyError:
                characters[c] = 1
            line += c
        lines.append(line)
    print("\n".join(lines))
    print(characters)


# copy from objects.maps.dimensions() but takes in array as positional
def dimensions(data, array=False):
    """Takes in a string map and returns a 2D list map and map dimensions"""
    if not array:
        data = [[col for col in row] for row in data.split('\n')]
    height = len(data)
    width = max(len(col) for col in data)
    return data, height, width

def gradient(x, y, characters, colors):
    """Returns a more realistic map color gradient"""
    return table(characters, blender(colors), x, y)

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
    ''' Ray Tracing Implementation based off of Rogue Basin Python Tutorial '''
    mult = [
                [1,  0,  0, -1, -1,  0,  0,  1],
                [0,  1, -1,  0,  0, -1,  1,  0],
                [0,  1,  1,  0,  0, -1, -1,  0],
                [1,  0,  0,  1, -1,  0,  0, -1]
            ]

    tile = namedlist("Tile", "char color bkgd light block_mov block_lit items")
    chars_block_move = {"#", "+", "o", "x", "~", "%", "Y", "T"}
    chars_block_move_hills =  {"#", "+", "o", "x", "%", "Y", "T"}
    chars_block_light = {"#", "+", "o", "%", "Y", "T"}
    # def __init__(self, data, map_type, map_id, width=80, height=50, cfg_path=None, map_name=None):
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.maptype = map_type

        # data holds the raw characters
        self.data, self.height, self.width = self.dimensions(data)
        self.map_id = map_id

        # Map Relationship with Player Entity
        self.relationship = 100 if self.maptype == "city" else -100
        if map_name:
            self.map_name = map_name

        # explicitely do not block "~" in hills
        self.block_chars = chars_block_move_hills if map_type == "hills" else chars_block_move
        self.block = [[self.data[y][x] in self.block_chars for x in range(self.width)] for y in range(self.height)]

        if cfg_path:
            self.units = self.populate(cfg_path)
        elif self.maptype == "dungeon":
            self.units = self.add_units(limit=15 if self.width >= 25 else 10)

        self.tilemap = self.fill(self.data, self.width, self.height)
        self.map_display_width = min(self.width, width)
        self.map_display_height = min(self.height, height)

        if map_init_debug:
            print('[MAP CLASS]:\n\t{}'.format(self.map_id))
            print("\tMAP DIM: {} {}".format(self.width, self.height))
            print("\tMAP DIS:{} {}".format(self.map_display_width, self.map_display_height))
 
    def build(self):
        raise NotImplementedError("cannot build the base map class")

    def __str__(self):
        return "\n".join("".join(row) for row in self.data)

    def __repr__(self):
        return "{}: ({}, {})".format(self.__class__.__name__, self.width, self.height)
    ###########################################################################
    # Level Initialization, Setup, Terraform and Evaluation                   #
    ###########################################################################
    def dimensions(self):
        '''takes in a string map and returns a 2D list map and map dimensions'''
        if hasattr(self, 'data'):
            self.height = len(self.data)
            self.width = max(len(col) for col in self.data)
        
    def fill(self, d, w, h):
        # Should only be called once by init
        def evaluate(char):
            try:
                if self.maptype not in ("dungeon", "city"):
                    t = self.wilderness[self.maptype][char]
                else:
                    t = self.landmarks[char]
            except KeyError:
                raise KeyError("Evaluate Map: {} not in keys".format(char))
            return t
        
        rows = []
        tiles = set()
        tree, ground = None, None
        d = d if isinstance(d, list) else d.split('\n')
        for row in d:
            cols = []
            for col in row:
                chars, hexcodes = evaluate(col)
                light = Light.Unexplored
                block_mov = col in self.block_chars
                block_lit = col not in chars_block_light
                tile = self.tile(
                    choice(chars), 
                    choice(hexcodes), 
                    "black", 
                    light, 
                    block_mov,
                    block_lit, 
                    [])
                tiles.add((tile.char, tile.block_mov, tile.block_lit))
                cols.append(tile)
            rows.append(cols)

        if debug:
            print('\tTiles - {}'.format(tiles))

        return rows        

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
        if debug:
            print('[GET DOWNSTAIRS]:')

        try:
            if hasattr(self, self.enterance):
                if debug:
                    print('\tMAP HAS ENTERANCE')

                return self.enterance
        except AttributeError:
            # manually look through the map to check for '>'
            for j in range(len(self.data)):
                for i in range(len(self.data[0])):
                    if self.data[j][i] == ">":

                        if debug:
                            print('\tHAS ENTERANCE AFTER LOOPING')
                            print(self.data[j][i], i, j)
                            print("\tLOCATION - {}, {}; CHAR - {}".format(
                                self.tilemap[j][i].char, i, j))

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

    def friendly(self):
        return self.relationship > 0
    ###########################################################################
    # Sight, Light and Color Functions                                        #
    ###########################################################################
    def lit(self, x, y):
        return self.square(x, y).light

    def set_lit(self, x, y, v):
        if self.within_bounds(x, y):
            self.square(x, y).light = v

    def lit_reset(self):
        for y in range(self.height):
            for x in range(self.width):
                if self.square(x, y).light:
                    self.square(x, y).light = 1 # if self.square(x, y).light > 0 else 0

    def fov_calc(self, lights):
        self.lamps = lights
        for x, y, radius in lights:
            for o in range(8):
                self.sight(x, y, 1, 1.0, 0.0, 
                        radius,
                        self.mult[0][o], 
                        self.mult[1][o], 
                        self.mult[2][o], 
                        self.mult[3][o], 0)

    def sight(self, cx, cy, row, start, end, radius, xx, xy, yx, yy, id):
        if start < end:
            return

        radius_squared = radius * radius

        for j in range(row, radius+1):

            dx, dy = -j-1, -j
            blocked = False
            while dx <= 0:
                dx += 1
                X, Y = cx + dx * xx + dy * xy, cy + dx * yx + dy * yy
                # l_slope and r_slope store the slopes of the left and right
                # extremities of the square we're considering:
                l_slope, r_slope = (dx-0.5)/(dy+0.5), (dx+0.5)/(dy-0.5)
                if start < r_slope:
                    continue
                elif end > l_slope:
                    break
                else:
                    # Our light beam is touching this square; light it:
                    if dx*dx + dy*dy < radius_squared:
                        self.set_lit(X, Y, 2)
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
                            self.sight(cx, cy, j+1, start, l_slope,
                                             radius, xx, xy, yx, yy, id+1)
                            new_start = r_slope
            # Row is scanned; do next row unless last square was blocked:
            if blocked:
                break
            
    ###########################################################################
    # Item object Functions                                                   #
    ###########################################################################
    def add_item(self, x, y, i):
        self.tilemap[y][x].items.append(i)
    ###########################################################################
    # Unit object Functions                                                   #
    ###########################################################################
    def reduce_relationship(self, reduce):
        self.relationship = min(-100, max(self.relationship - reduce, 100))

    def increase_relationship(self, increase):
        self.relationship = min(-100, max(self.relationship - increase, 100))
        return "Your relationship with {} has decreased by {}".format(
            self.map_name)
    ###########################################################################
    # Unit object Functions                                                   #
    ###########################################################################
    def get_unit(self, x, y):
        if hasattr(self, 'units'):
            for u in self.units:
                if (x, y) == u.position():
                    return u

    def get_units(self):
        if hasattr(self, 'units'):
            return self.units
        return []

    def get_unit_positions(self):
        if hasattr(self, 'units'):
            return {u.position() for u in self.units}
        return {}

    def remove_unit(self, unit):
        if hasattr(self, 'units'):
            self.units.remove(unit)

    ###########################################################################
    # Output and Display Functions                                            #
    ###########################################################################
    def output(self, player_x, player_y, units):
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
                    lit = self.lit(x, y)
                    if lit == 2:
                        ch = positions[(x, y)].character
                        col = positions[(x, y)].color
                    elif lit == 1:
                        ch, col = self.square(x, y).char, 'darkest grey'
                    else:
                        ch, col = " ", "black"


                # Current position holds an item
                    # elif self.square(x, y).items:
                    #     if self.lit(x, y):
                    #         item = choice(self.square(x, y).items)
                    #         level = ""
                    #         ch = item.char
                    #         col = item.color
                    #     else:
                    #         level = ""
                    #         ch = " "
                    #         lit = "black"

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
                    lit = self.lit(x, y)
                    if lit == 2:
                        ch = self.square(x, y).char
                        col = self.square(x, y).color
                    elif lit == 1:
                        ch = self.square(x, y).char
                        col = "darkest grey"
                    else:
                        ch, col = " ", "black"

                yield (x-cam_x, y-cam_y, col, ch)
        self.lit_reset()

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