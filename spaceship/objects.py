import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))+'/../')
from namedlist import namedlist
from collections import namedtuple
from spaceship.imports import *
from spaceship.colors import color, COLOR, SHIP_COLOR
from random import randint, choice
from math import sqrt
from spaceship.constants import GAME_SCREEN_HEIGHT as sh
from spaceship.constants import GAME_SCREEN_WIDTH as sw
from spaceship.maps import hextup, hexone, output, blender, gradient, evaluate_blocks
from spaceship.setup import toInt, palette
from spaceship.charmap import Charmap as cm
# TODO: Maybe move map to a new file called map and create a camera class?

errormessage=namedtuple("ErrMsg", "x y ch lvl vis lit")
symboltype = namedtuple("Symbol", "ascii unicode")
visibility = namedtuple("Visiblity", "movement visibility lightlevel")

class Light: Unexplored, Explored, Visible = range(3)    
class Letter: Ascii, Unicode = range(2)

# fog levels are calculated in steps of 2, so radius of 10/11 will be the max bounds
fog_levels= ["darkest ", "darker ", "dark ","light ","lighter ", "lightest"]

chars_roads= [":"]
chars_floor= ["."]
chars_block= ("#", "+", "o", "x", "~", "%")
chars_grass= [",",";",]
chars_water= ["~"]
chars_house= ["="]
chars_walls= ["#"]
chars_doors= ["+", "/"]
chars_plant= ["2663"]
chars_posts= ["x"]
chars_lamps= ["o"]

class Player:
    def __init__(self, character, x, y):
        # unpack everything here
        self.name = character.name[0].upper() + character.name[1:]
        self.home = self.location = character.home
        self.gold = character.gold
        self.level = 1
        self.exp = 0
        self.advexp = 80
        self.x, self.y = x, y
        self.base_stats = character.stats
        self.gender = character.gender
        self.gender_bonus = character.gbonus
        self.race = character.race
        self.race_bonus = character.rbonus
        self.job = character.job
        self.job_bonus = character.jbonus
        self.skills = character.skills
        self.equipment = character.eq
        self.inventory = character.inv
        self.sight = 25
        self.calculate_initial_stats()

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

    def move(self, dx, dy):
        self.x += dx
        self.y += dy

    def pos(self):
        return self.x, self.y

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
            Subrace  : {}
            Class    : {}
            Subclass : {}

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
            {}
            ========  Alignments  ========
            ========  Relations   ========
            """[1:]
        print(self.backpack.dump())
        print(dump_template.format(
            stat.format("Hero"),
            stat.format("Male"),
            stat.format("Human"),
            stat.format("Redskin"),
            stat.format("Rogue"),
            stat.format("Ninja"),
            expe.format("3"),
            expe.format("25"),
            self.backpack.dump(),
        ))

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

    colors_block = ["#ffc0c0c0", "#ffa0a0a0", "#ff808080", "#ff606060", "#ff404040"]
    # colors_water = blender(color_water, 20)

    def __init__(self, data, GW=80, GH=40):
        self.SUN = True
        # self.data, self.height, self.width = self.dimensions(data)
        self.data, self.height, self.width = self.dimensions(data)
        for i in self.data:
            print(i)
        print("MAP: {} {}".format(self.width, self.height))
        # self.block blocks both light (and movement?)
        self.light = [[0 for _ in range(self.width)] for _ in range(self.height)]
        self.lamps = None
        self.fogofwar=[[0 for _ in range(self.width)] for _ in range(self.height)]
        # self.block only blocks movements
        self.block = [[self.data[y][x] in chars_block for x in range(self.width)] for y in range(self.height)]
        # self.walls = gradient(self.width, self.height, chars_walls, color_walls)
        # self.grass = gradient(self.width, self.height, chars_grass, color_grass)
        # self.plant = gradient(self.width, self.height, chars_plant, color_plant)
        self.map_display_width = min(self.width, sw-12)
        self.map_display_height = min(self.height, sh-8)
        self.tilemap = self.fill(data, self.width, self.height)
        self.explore = [[0 for _ in range(self.width)] for _ in range(self.height)]
        print("MAP: {} {}".format(self.map_display_width, self.map_display_height))
 

    @staticmethod
    def dimensions(data):
        '''takes in a string map and returns a 2D list map and map dimensions'''
        if isinstance(data, str):
            data = [[col for col in row] for row in data.split('\n')]
        height = len(data)
        width = max(len(col) for col in data)
        # return data, height, width
        return data, height, width

    def start_position(self):
        for i in range(len(self.data)):
            for j in range(len(self.data[0])):
                if self.data[i][j] == "<":
                    return (j, i)

    def fill(self, d, w, h):
        # Light.Unexplored, Explored, Visible
        tile = namedlist("Tile", "char color bkgd visible walkable items")
        locchar={
            ".": (cm.TILES.chars, blender(cm.TILES.hexcode), "black"),
            ",": (cm.GRASS.chars, blender(cm.GRASS.hexcode), "black"),
            "#": (cm.WALLS.chars, blender(cm.WALLS.hexcode), "black"),
            "~": (cm.WATER.chars, blender(cm.WATER.hexcode), "black"),
            "+": (cm.DOORS.chars, blender(cm.DOORS.hexcode), "black"),
            "x": (cm.POSTS.chars, blender(cm.POSTS.hexcode), "black"), 
            "|": (cm.PLANT.chars, blender(cm.PLANT.hexcode), "black"),
            "o": (cm.LAMPS.chars, blender(cm.LAMPS.hexcode), "black"),
            ":": (cm.ROADS.chars, blender(cm.ROADS.hexcode), "black"),
            "=": (cm.HOUSE.chars, blender(cm.HOUSE.hexcode), "black"),
            " ": (' ', '#000000',"black"),
            "%": (cm.WALLS.chars, blender(cm.WALLS.hexcode), "black"),
            "^": (cm.WALLS.chars, blender(cm.WALLS.hexcode), "black"),
            "<": (cm.WALLS.chars, blender(cm.WALLS.hexcode), "black"),
            ">": (cm.WALLS.chars, blender(cm.WALLS.hexcode), "black"),
        }

        def evaluate(char):
            try:
                t = locchar[char]
            except KeyError:
                pass
            return t
        
        rows = []
        for row in d.split('\n'):
        # for row in d:
            cols = []
            for col in row:
                chars, hexcodes, bkgd = evaluate(col)
                light = Light.Unexplored
                walkable = col in chars_block
                cols.append(tile(choice(chars), choice(hexcodes), bkgd, light, walkable, []))
            rows.append(cols)
        return rows

    def add_item(self, x, y, i):
        self.tilemap[y][x].items.append(i)

    def square(self, x, y):
        # return self.data[y][x]
        return self.tilemap[y][x]

    def _sunup(self):
        self.SUN=True


    def _sundown(self):
        self.SUN=False

    def darken(self, color):
        color = color[3:]
        if color == "656565":
            return "#323232"
        elif color == "888888":
            return "#444444"
        elif color == "989898":
            return "#494949"
        elif color == "b0b0b0":
            return "#555555"

    def open_door(self, x, y):
        # if self.square(x, y) == "+":
        #     self.data[y][x] = "/"
        openable = self.tilemap[y][x].char == "+"
        if openable:
            self.tilemap[y][x].char = "/"

    
    def close_door(self, x, y):
        # if self.square(x, y) == "/":
        #     self.data[y][x] = "+"
        closeable = self.tilemap[y][x].char == "/"
        if closeable:
            self.tilemap[y][x].char = "+"

    def reblock(self, x, y):
        self.block[y][x] = True

    def unblock(self, x, y):
        self.block[y][x] = False

    def blocked(self, x, y):
        return (x < 0 or y < 0 or x >= self.width 
                or y >= self.height or self.tilemap[y][x].char in ("#", "+", "%"))

    def explored(self, x, y):
        return self.explore[y][x] > 0

    def _sun(self):
        return self.SUN

    def lit(self, x, y):
        #return self.light[y][x] == self.flag
            return self.light[y][x]

    def lit_level(self, x, y):
        return self.light[y][x]

    def set_lit(self, x, y, v):
        if 0 <= x < self.width and 0 <= y < self.height:
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
                        if self.blocked(X, Y):
                            new_start = r_slope
                            continue
                        else:
                            blocked = False
                            start = new_start
                    else:
                        if self.blocked(X, Y) and j < radius:
                            # This is a blocking square, start a child scan:
                            blocked = True
                            self.sight(cx, cy, j+1, start, l_slope,
                                             radius, xx, xy, yx, yy, id+1)
                            new_start = r_slope
            # Row is scanned; do next row unless last square was blocked:
            if blocked:
                break
            
    def output(self, X, Y, units):

        # character checks
        def isWalls(c): return c in chars_walls
        def isPosts(c): return c in chars_posts
        def isDoors(c): return c in chars_doors
        def isLamps(c): return c in chars_lamps
        def isRoads(c): return c in chars_roads
        def isWater(c): return c in chars_water
        def isPlant(c): return c in chars_plant
        def isGrass(c): return c in chars_grass
        def isHouse(c): return c in chars_house
        def isFloor(c): return c in chars_floor

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
        cx = scroll(X, self.map_display_width, self.width)
        cy = scroll(Y, self.map_display_height, self.height)
        cxe = cx + self.map_display_width
        cye = cy + self.map_display_height

        #fg_fog = "#ff202020"
        # daytime= True if self._sun() else False
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
                # need to check if light is out
                # if daytime:
                #     # sun causes everything to be lit
                #     lit = fog_levels[3]
                #     level = ""
                # else:
                #     # check if the square is lighted and the light strength
                #     lit = self.lit(x, y)
                #     level = fog_levels[3]

                #blocks are visible if the sun is up or in range of a lightable object
                # visible = lit
                #level = fog_levels[max(5-level, 0)] if level else fog_levels[min(0, level)]

                if x == X and y == Y:
                    # Current position holds your position
                    ch = "@"
                    col = "white"

                elif (x, y) in positions.keys():
                    # Current position holds a unit
                    lit = self.lit(x, y)
                    ch = positions[(x, y)].i
                    col = positions[(x, y)].c if lit == 2 else "black"

                #     if daytime:
                #         level = ""
                #         unit = positions[(x,y)]
                #         ch = unit.i
                #         col = unit.c

                #     else:
                #         level = "" if visible else "darkest "
                #         ch = "@" if visible else self.square(x, y).char
                #         col = "orange" if visible else fg_fog

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

                # all other environment features
                else:
                    lit = self.lit(x, y)
                    if lit:
                        if lit == 2:
                            ch, col, _, _, _, _ = self.square(x, y)
                            # col = "white"
                        else:
                            ch, _, _, _, _, _ = self.square(x, y)
                            col = "darkest grey"
                    else:
                        ch, col, bkgd = " ", "black", None

                ch = ch if len(str(ch)) > 1 else chr(toInt(palette[ch]))

                try:        
                    yield (x-cx, y-cy, col, ch, None)
                except NameError:
                    yield (x-cx, y-cy, col, ch, None)
        self.lit_reset()
