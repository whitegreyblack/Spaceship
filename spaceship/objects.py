import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))+'/../')
from namedlist import namedlist
from collections import namedtuple
from spaceship.imports import *
from spaceship.colors import Color
from random import randint, choice
from math import sqrt
from spaceship.constants import GAME_SCREEN_HEIGHT as sh
from spaceship.constants import GAME_SCREEN_WIDTH as sw
from spaceship.maps import hextup, hexone, output, blender, gradient, evaluate_blocks
from spaceship.setup import toInt
from spaceship.charmap import DungeonCharmap as dcm
from spaceship.charmap import WildernessCharmap as wcm
from spaceship.world import World
# TODO: Maybe move map to a new file called map and create a camera class?

errormessage=namedtuple("ErrMsg", "x y ch lvl vis lit")
symboltype = namedtuple("Symbol", "ascii unicode")
visibility = namedtuple("Visiblity", "movement visibility lightlevel")

class Light: Unexplored, Explored, Visible = range(3)    
class Letter: Ascii, Unicode = range(2)

# change variables to dictioanry -- more tight and accessible
# allows for more 
chars_key = {
    "roads": [":"],
    "floor": ["."],
    "water": ["~"],
    "grass": [",",";"],
    "doors": ["+", "/"],
    "walls": ["#"],
    "posts": ["x"],
    "lamps": ["o"],
    "plant": ["2663"],
    "house": ["="],
}

chars_block_move= {"#", "+", "o", "x", "~", "%", "Y", "T"}
chars_block_light = {"#", "+", "o", "%", "Y", "T"}

class Player:
    def __init__(self, character):
        # unpack everything here
        self.exp = 0
        self.level = 1
        self.sight = 12
        self.advexp = 80
        self.job = character.job
        self.race = character.race
        self.gold = character.gold
        self.gender = character.gender
        self.skills = character.skills
        self.base_stats = character.stats
        self.job_bonus = character.jbonus
        self.race_bonus = character.rbonus
        self.equipment = character.equipment
        self.inventory = character.inventory
        self.gender_bonus = character.gbonus
        self.name = character.name[0].upper() + character.name[1:]

        # functions after unpacking
        self.setupHome(character.home)
        self.calculate_initial_stats()

    def setupHome(self, home):
        self.home, self.hpointer = home, World.capitals(home)
        self.wx, self.wy = self.hpointer
        self.zAxis = -1

    def worldPosition(self):
        return self.wx, self.wy

    def saveWorldPos(self):
        self.lastWorldPosition = self.wx, self.wy

    def mapPosition(self):
        return self.mx, self.my

    def saveMapPos(self):
        self.lastMapPosition = self.mx, self.my

    def resetMapPos(self, x, y):
        self.mx, self.my = x, y

    def getWorldPosOnEnter(self):
        if not hasattr(self, "lastWorldPosition"):
            raise AttributeError("Cant call this func without a lastWorldPosition")

        def direction(x, y):
            return (x+1)/2, (y+1)/2

        try:
            print(self.wx - self.lastWorldPosition[0], self.wy - self.lastWorldPosition[1])
            print(self.lastWorldPosition[0]-self.wx, self.lastWorldPosition[1]-self.wy)
            print(direction(self.wx - self.lastWorldPosition[0], self.wy - self.lastWorldPosition[1]))
            return direction(self.lastWorldPosition[0]-self.wx, self.lastWorldPosition[1]-self.wy)
        except KeyError:
            raise KeyError("direction not yet added or calculations were wrong")
    

    def calculate_initial_stats(self):
        stats = tuple(s+g+r+c for s , g, r, c 
                            in zip(self.base_stats,
                                   self.gender_bonus,
                                   self.race_bonus,
                                   self.job_bonus))
        
        self.str, self.con, self.dex, self.int, self.wis, self.cha = stats
        self.hp = self.total_hp = self.str+self.con*2
        self.mp = self.total_mp = self.int*self.wis*2
        self.sp = self.dex//5

    def moveOnMap(self, dx, dy):
        self.mx += dx
        self.my += dy
    
    def moveOnWorld(self, dx, dy):
        self.wx += dx
        self.wy += dy

    def moveZAxis(self, move):
        def checkZAxis(move):
            '''Make sure Z-Axis not less than -1 (WorldViewIndex)'''
            return max(self.zAxis+move, -1)

        self.zAxis = checkZAxis(move)

    def dump(self):
        GREEN='\x1b[1;32;40m'
        RED='\x1b[1;31;40m'
        BLUE='\x1b[0;34;40m'
        YELLOW='\x1b[0;33;40m'
        END='\x1b[0m'
        ISATTY = sys.stdout.isatty()
        stat = GREEN+"{:<7}"+END if ISATTY else "{}"
        expe = BLUE+"{:>7}"+END if ISATTY else "{}"
        dump_template="""
            [Character Sheet -- Spaceship]
            ======== Player Stats ========
            Name     : {}
            Sex      : {}
            Race     : {}
            Class    : {}

            Level    : {}
            Exp      : {}
            ========   Equipment  ========
            Head     :
            Neck     : 
            Torso    : Peasant garb
            Ring(L)  :
            Hand(L)  : Sword
            Ring(R)  :
            Hand(R)  : 
            Waist    : Thin rope
            Legs     : Common pants
            Feet     : Sandals
            ======== Player Items ========
            ========  Alignments  ========
            ========  Relations   ========
            """[1:]
        # print(self.backpack.dump())
        print(dump_template.format(
            self.name,
            self.gender,
            self.race,
            self.job,
            self.level,
            self.exp,
        ))

class Item:
    def __init__(self, n, s, c):
        self.name = n
        self.char = s
        self.color = c

    def classifier(self):
        pass

class Object:
    def __init__(self, n, x, y, i, c='white', r="human", h=10):
        """@parameters :- x, y, i, c
            x: positional argument,
            y: positional argument,
            i: char/image for object representation,
            c: color for object fill
        """
        self.name = n
        self.x = x
        self.y = y
        self.i = i
        self.c = c
        self.r = r
        self.h = h
        self.message = "Im just an object"

    def move(self, dx, dy):
        self.x += dx
        self.y += dy

    def talk(self):
        return self.name + ": " +self.message

    def draw(self):
        return (self.x, self.y, self.i, self.c)

    def pos(self):
        return self.x, self.y

class Character(Object):
    def __init__(self, n, x, y, i, c='white', r='human', m=10, s=10, b=6, l=5):
        super().__init__(n, x, y, i, c, r)
        self.m=m
        self.s=s
        self.l=l
        self.inventory = Inventory(b)
        self.backpack = Backpack()

class Slot:
    def __init__(self, current=None):
        self._slot = current

    @property
    def slot(self):
        return self._slot

    @slot.setter
    def slot(self, item):
        self._slot = item
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
    
    tile = namedlist("Tile", "char color bkgd visible block_mov block_lit items")

    def __init__(self, data, maptype, GW=80, GH=40):
        self.maptype = maptype
        self.data, self.height, self.width = self.dimensions(data)
        print("MAP: {} {}".format(self.width, self.height))
        self.light = [[0 for _ in range(self.width)] for _ in range(self.height)]
        self.block = [[self.data[y][x] in chars_block_move for x in range(self.width)] for y in range(self.height)]
        self.tilemap = self.fill(data, self.width, self.height)
        self.map_display_width = min(self.width, GW)
        self.map_display_height = min(self.height, GH)
        print("MAP: {} {}".format(self.map_display_width, self.map_display_height))
 
    ###########################################################################
    # Level Initialization, Setup and Evaluation                              #
    ###########################################################################
    @staticmethod
    def dimensions(data):
        '''takes in a string map and returns a 2D list map and map dimensions'''
        if isinstance(data, str):
            data = [[col for col in row] for row in data.split('\n')]
        height = len(data)
        width = max(len(col) for col in data)
        # return data, height, width
        return data, height, width

    def fill(self, d, w, h):
        # Light.Unexplored, Explored, Visible
        # city, wilderness, dungeon
        plainschar = {
            ".": (wcm.GRASS.chars, blender(wcm.GRASS.hexcode)),
            ",": (wcm.GRASS.chars, blender(wcm.GRASS.hexcode)),
            ";": (wcm.GRASS.chars, blender(wcm.GRASS.hexcode)),
            "`": (wcm.GRASS.chars, blender(wcm.GRASS.hexcode)),
            "\"": (wcm.GRASS.chars, blender(wcm.GRASS.hexcode)),
            # "Y": (wcm.TREES.chars, blender(wcm.TREES.hexcode)),
            "T": (choice(wcm.TREES.chars), blender(wcm.TREES.hexcode)),
            # "f": (wcm.TREES.chars, blender(wcm.TREES.hexcode)),
            "~": (wcm.HILLS.chars, blender(wcm.HILLS.hexcode)),
        }

        locchar={
            ".": (dcm.TILES.chars, blender(dcm.TILES.hexcode)),
            ",": (dcm.GRASS.chars, blender(dcm.GRASS.hexcode)),
            "#": (dcm.WALLS.chars, blender(dcm.WALLS.hexcode)),
            "~": (dcm.WATER.chars, blender(dcm.WATER.hexcode)),
            "+": (dcm.DOORS.chars, blender(dcm.DOORS.hexcode)),
            "x": (dcm.POSTS.chars, blender(dcm.POSTS.hexcode)), 
            "|": (dcm.PLANT.chars, blender(dcm.PLANT.hexcode)),
            "o": (dcm.LAMPS.chars, blender(dcm.LAMPS.hexcode)),
            ":": (dcm.ROADS.chars, blender(dcm.ROADS.hexcode)),
            "=": (dcm.HOUSE.chars, blender(dcm.HOUSE.hexcode)),
            " ": (' ', '#000000'),
            "%": (dcm.WALLS.chars, blender(dcm.WALLS.hexcode)),
            "^": (dcm.WALLS.chars, blender(dcm.WALLS.hexcode)),
            "<": (dcm.LTHAN.chars, blender(dcm.LTHAN.hexcode)),
            ">": (dcm.GTHAN.chars, blender(dcm.GTHAN.hexcode)),
            "^": (dcm.TRAPS.chars, blender(dcm.TRAPS.hexcode)),
        }

        def evaluate(char):
            try:
                if self.maptype == "plains":
                    t = plainschar[char]
                elif self.maptype == "hills":
                    t = plainschar[char]
                else:
                    t = locchar[char]
            except KeyError:
                raise KeyError("Evaluate Plains Map: {} not in keys".format(char))
            return t
        
        rows = []
        d = d if isinstance(d, list) else d.split('\n')
        tiles = set()
        for row in d:
        # for row in d:
            cols = []
            for col in row:
                chars, hexcodes = evaluate(col)
                light = Light.Unexplored
                block_mov = col in chars_block_move
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
        for i in tiles:
            print(i)
        return rows

    ###########################################################################
    # Connected Map/Dungeon Functions and Properties                          #
    ###########################################################################
    def getExit(self):
        '''find exit and save on the first time
        subsequent calls returns the saved point'''
        if hasattr(self, "exitpoint"):
            print('has exit')
            print(self.exitpoint)
            return self.exitpoint

        for j in range(len(self.data)):
            for i in range(len(self.data[0])):
                if self.data[j][i] == "<":
                    print('GetExit')
                    print(self.data[j][i], i, j)
                    print(self.tilemap[j][i].char, i, j)
                    self.exitpoint = i, j
                    return i, j

    def getEntrance(self):
        '''same logic as getExit'''
        try:
            if hasattr(self, self.enterance):
                print('has enterance')
                return self.enterance
        except AttributeError:
            for j in range(len(self.data)):
                for i in range(len(self.data[0])):
                    if self.data[j][i] == ">":
                        print('GetEnterance')
                        print(self.data[j][i], i, j)
                        print(self.tilemap[j][i].char, i, j)
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
        return self.within_bounds(x, y) and not self.square(x, y).block_mov

    def viewable(self, x, y):
        '''Only acts on objects within the bounds of the map'''
        return self.within_bounds(x, y) and self.square(x, y).block_lit

    def blocked(self, x, y):
        '''Only acts on objects within the bounds of the map'''
        return self.out_of_bounds(x, y) or self.square(x, y).block_mov

    def open_door(self, x, y):
        def is_closed_door(x, y):
            return self.square(x,y).char == "+"
        # if self.square(x, y) == "+":
        #     self.data[y][x] = "/"
        if is_closed_door(x, y):
            self.tilemap[y][x].char = "/"

    def close_door(self, x, y):
        def is_opened_door(x, y):
            return self.square(x, y).char == "/"
        # if self.square(x, y) == "/":
        #     self.data[y][x] = "+"
        if is_opened_door(x, y):
            self.tilemap[y][x].char = "+"

    def reblock(self, x, y):
        # self.block[y][x] = True
        self.square(x, y).block_mov = True

    def unblock(self, x, y):
        # self.block[y][x] = False
        self.square(x, y).block_mov = False

    ###########################################################################
    # Sight, Light and Color Functions                                        #
    ###########################################################################
    def darken(self, color):
        color = color[3:] # removes "#ff" -> hexcode identifier and alpha channel
        if color == "656565":
            return "#323232"
        elif color == "888888":
            return "#444444"
        elif color == "989898":
            return "#494949"
        elif color == "b0b0b0":
            return "#555555"

    def lit(self, x, y):
        #return self.light[y][x] == self.flag
            return self.light[y][x]

    def lit_level(self, x, y):
        return self.light[y][x]

    def set_lit(self, x, y, v):
        if self.within_bounds(x, y):
            self.light[y][x] = v
        # def set_lit(self, x, y, row, radius):
        #     if 0 <= x < self.width and 0 <= y < self.height:
        #         if self.light[y][x] < radius-row:
        #             self.light[y][x] = radius-row
        #             self.fogofwar[y][x] = True

    def lit_reset(self):
        self.light = [[1 if self.light[y][x] > 0 else 0 for x in range(self.width)] for y in range(self.height)]
    
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
    # Item and Object Functions                                               #
    ###########################################################################
    def add_item(self, x, y, i):
        self.tilemap[y][x].items.append(i)

    ###########################################################################
    # Output and Display Functions                                            #
    ###########################################################################
    def output(self, X, Y, units):

        def scroll(position, screen, worldmap):
            """
            @position: current position of player 1D axis
            
            @screen  : size of the screen
            
            @worldmap: size of the map           
            """
            halfscreen = screen//2
            # less than half the screen - nothing
            if position < halfscreen:
                return 0
            elif position >= worldmap - halfscreen:
                return worldmap - screen
            else:
                return position - halfscreen

        # print(self.map_display_height, self.map_display_width)
        # print(self.height, self.width)
        cx = scroll(X, self.map_display_width-14, self.width)
        cy = scroll(Y, self.map_display_height-2, self.height)
        cxe = cx + self.map_display_width-14
        cye = cy + self.map_display_height-2
        print(cx, cxe)
        print(cy, cye)
        daytime = False
        fg_fog = "grey"
        bg_fog = "#ff000000"
        positions = {}
        for unit in units:
            positions[unit.pos()] = unit

        col = "#ffffff"
        # width should total 80 units
        for x in range(cx, cxe):

            # height should total 24 units
            for y in range(cy, cye):

                if x == X and y == Y:
                    # Current position holds your position
                    ch = "@"
                    col = "white"

                elif (x, y) in positions.keys():
                    # Current position holds a unit
                    lit = self.lit(x, y)
                    ch = positions[(x, y)].i
                    col = positions[(x, y)].c if lit == 2 else "black"

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

                # # Current position holds a Lamp
                # elif (x, y, 10) in self.lamps:
                #     level = ""
                #     ch = self.square(x, y).char
                #     col = "white"

                else:
                    # all other environment features
                    lit = self.lit(x, y)
                    if lit:
                        if lit == 2:
                            ch = self.square(x, y).char
                            col = self.square(x, y).color
                            # col = "white"
                        else:
                            ch = self.square(x, y).char
                            col = "darkest grey"
                    else:
                        ch, col, bkgd = " ", "black", None

                # ch = ch if len(str(ch)) > 1 else chr(toInt(palette[ch]))

                try:        
                    yield (x-cx, y-cy, col, ch, None)
                except NameError:
                    yield (x-cx, y-cy, col, ch, None)
        self.lit_reset()
