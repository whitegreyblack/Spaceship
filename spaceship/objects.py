import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))+'/../')
from collections import namedtuple
from spaceship.imports import *
from spaceship.colors import color, COLOR, SHIP_COLOR
from random import randint, choice
from spaceship.constants import SCREEN_HEIGHT as sh
from spaceship.constants import SCREEN_WIDTH as sw
from spaceship.maps import hextup, hexone, output, blender, gradient, evaluate_blocks
# TODO: Maybe move map to a new file called map and create a camera class?


errormessage=namedtuple("ErrMsg", "x y ch lvl vis lit")

class Light: Unexplored, Explored, Visible = range(3)    

# fog levels are calculated in steps of 2, so radius of 10/11 will be the max bounds
fog_levels= {
    0: "darkest ",
    1: "darker ",
    2: "dark ",
    3: "light ",
    4: "lighter ",
    5: "lightest",
}

chars={
    "grass": ([",",";","`"], ("#56ab2f", "#a8e063")),
    "walls": (["#"], ("#eacda3", "#d6ae7b")),
    "doors": (["+"], ("#ff994C00", "#ff994C00")),
    "brick": (["%"], ("#a73737", "#7a2828"))
}

chars_grass= [",",";",]
chars_walls= ["#"]
chars_doors= ["+"]
chars_plant= ["2663"]
color_grass=("#56ab2f", "#a8e063")
color_walls=("#eacda3", "#d6ae7b")
color_plant=("#FDFC47", "##24FE41")
#color_walls=("#a73737", "#7a2828")
class Object:
    def __init__(self, x, y, i, c='white'):
        """@parameters :- x, y, i, c
            x: positional argument,
            y: positional argument,
            i: char/image for object representation,
            c: color for object fill
        """
        self.x = x
        self.y = y
        self.i = i
        self.c = c

    def move(self, dx, dy):
        self.x += dx
        self.y += dy

    def draw(self):
        return (self.x, self.y, self.i, self.c)

    def pos(self):
        return self.x , self.y

class Person(Object):
    def __init__(self, x, y, i, c='white'):
        super().__init__(x, y, i, c)
        self.h = 100
        self.m = 100
        self.s = 100

    def stats(self):
        return self.h, self.m, self.s

    def draw(self):
        prev = list(super().draw())
        return tuple(prev+[self.h, self.m, self.s])
    
class Map:
    ''' Ray Tracing Implementation based off of Rogue Basin Python Tutorial '''
    mult = [
                [1,  0,  0, -1, -1,  0,  0,  1],
                [0,  1, -1,  0,  0, -1,  1,  0],
                [0,  1,  1,  0,  0, -1, -1,  0],
                [1,  0,  0,  1, -1,  0,  0, -1]
            ]

    colors_block = ["#ffc0c0c0", "#ffa0a0a0", "#ff808080", "#ff606060", "#ff404040"]
    colors_water = blender("#43C6AC", "#191654", 20)

    def __init__(self, data):
        self.SUN = False
        self.data, self.height, self.width = self.dimensions(data)
        # self.block blocks both light (and movement?)
        self.light = [[0 for _ in range(self.width)] for _ in range(self.height)]
        self.lamps = None
        self.fogofwar=[[0 for _ in range(self.width)] for _ in range(self.height)]
        # self.block only blocks movements
        self.block = [[self.data[y][x] in ("#", "+", "o", "x") for x in range(self.width)] for y in range(self.height)]
        self.walls = gradient(self.width, self.height, chars_walls, color_walls)
        self.grass = gradient(self.width, self.height, chars_grass, color_grass)
        self.plant = gradient(self.width, self.height, chars_plant, color_plant)
        self.flag = 0
        self.map_display_width = min(self.width, sw-20)
        self.map_display_height = min(self.height, sh-6)

    @staticmethod
    def dimensions(data):
        '''takes in a string map and returns a 2D list map and map dimensions'''
        data = [[col for col in row] for row in data.split('\n')]
        height = len(data)
        width = max(len(col) for col in data)
        return data, height, width

    def square(self, x, y):
        return self.data[y][x]


    def openable(self, x, y, ch):
        return self.square(x,y) == "+"

    def _sunup(self):
        self.SUN=True

    def _sundown(self):
        self.SUN=False

    def open_door(self, x, y):
        if self.square(x, y) == "+":
            self.data[y][x] = "/"
    

    def close_door(self, x, y):
        if self.square(x, y) == "/":
            self.data[y][x] = "+"


    def reblock(self, x, y):
        self.block[y][x] = True


    def unblock(self, x, y):

        self.block[y][x] = False


    def blocked(self, x, y):
        return (x < 0 or y < 0 or x >= self.width 
                or y >= self.height or self.data[y][x] in ("#", "+",))

    def _sun(self):
        return self.SUN


    def lit(self, x, y):
        #return self.light[y][x] == self.flag
        return self.light[y][x] > 0

    def lit_level(self, x, y):
        return self.light[y][x]
    """
    def set_lit(self, x, y):
        if 0 <= x < self.width and 0 <= y < self.height:
            self.light[y][x] = self.flag
    """
    def set_lit(self, x, y, row):
        if 0 <= x < self.width and 0 <= y < self.height:
            if self.light[y][x] < 10-row:
                self.light[y][x] = 10-row
                self.fogofwar[y][x] = True

    def lit_reset(self):
        self.light = [[0 for _ in range(self.width)] for _ in range(self.height)]

    #def fov_calc(self, x, y, radius):
    def fov_calc(self, lights):
        self.lamps = lights
        self.flag += 1
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
                        #self.set_lit(X, Y)
                        self.set_lit(X, Y, j)
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
        def scroll(p, s, m):
            """@p: current position of player 1D
            @s: size of the screen
            @m: size of the map           
            """
            hs = s//2
            if p < hs:
                return 0
            elif p >= m - hs:
                return m - s
            else:
                return p - hs

        cx = scroll(X, self.map_display_width, self.width)
        cy = scroll(Y, self.map_display_height, self.height)
        cxe = cx + self.map_display_width
        cye = cy + self.map_display_height

        #fg_fog = "#ff202020"
        daytime= True if self._sun() else False

        fg_fog = "grey"
        bg_fog = "#ff000000"
        positions = {}
        for unit in units:
            positions[unit.pos()] = unit

        # width should total 80 units
        for x in range(cx, cxe):

            # height should total 24 units
            for y in range(cy, cye):
                # need to check if light is out
                if daytime:
                    # sun causes everything to be lit
                    lit = fog_levels[3]
                    level = ""
                else:
                    # check if the square is lighted and the light strength
                    lit = self.lit(x, y)
                    level = fog_levels[min(self.lit_level(x, y)//2, 5)]

                #blocks are visible if the sun is up or in range of a lightable object
                visible = daytime or lit
                #level = fog_levels[max(5-level, 0)] if level else fog_levels[min(0, level)]

                if x == X and y == Y:
                    level = ""
                    ch = "@"
                    lit = "white"
                    ## bkgd = "black"

                elif (x, y) in positions.keys():
                    if daytime:
                        level = ""
                        unit = positions[(x,y)]
                        ch = unit.i
                        lit = unit.c

                    else:
                        level = "" if visible else "darkest "
                        ch = "@" if visible else self.square(x, y)
                        lit = "orange" if visible else fg_fog
                    
                elif (x, y, 5) in self.lamps:
                    level = ""
                    ch = "!"
                    lit = "white"

                else:
                    flag = ""
                    lit = self.lit_level(x, y)
                    level = ""
                    ch = self.square(x, y)
                    flag = ch

                    # then try to color according to block type
                    # color the floor
                    if len(str(ch)) < 2:
                        if ch in (".",):
                            #_, color, _, _ = self.stone[y][x]
                            #lit = "white" if lit else fog
                            #lit = hexone(color//2) if visible else fg_fog
                            level = fog_levels[lit//2] if not daytime else "darkest " 
                            lit = "grey" if visible else "black"
                            ## bkgd = "black" if not lit else bg_fog
                        if ch in (":",):
                            #_, color, _, _ = self.stone[y][x]
                            #lit = "white" if lit else fog
                            #lit = hexone(color//2) if visible else fg_fog
                            level = fog_levels[lit//2] if not daytime else "" 
                            lit =  "#9a8478" if visible else fg_fog
                            ## bkgd = "black" if not lit else bg_fog
                        # color some grasses
                        if ch in (",",";","!","`"):
                            ch, col, _, _ = self.grass[y][x]
                            #lit = hextup(color,5,2,5) if visible else fg_fog
                            # bkgd = hextup(color, 5,3,5) if lit else bg_fog
                            level = fog_levels[lit//2] if not daytime else "" 
                            lit = col if visible else fg_fog

                        # color the water
                        if ch == "~":
                            lit = choice(self.colors_water) if visible else fg_fog

                        # color the doors
                        if ch in ("+", "/",):
                            lit = "#ff994C00" if visible else fg_fog
                            # bkgd = "black"i

                        # color the lamps
                        if ch in ("o",):
                            lit = "white" if visible else fg_fog

                        # color the walls
                        if ch == "#":
                            _, color, _, _ = self.walls[y][x]
                            #lit = hexone(color) if visible else fg_fog
                            lit = color if visible else fg_fog
                            # bkgd = "grey" if lit else bg_fog
                            #lit = "white" if lit else fog
                        
                        if ch == "%":
                            _, color, _, _ = self.walls[y][x]
                            #lit = hexone(color//2) if lit else fg_fog
                            lit = color if visible else fg_fog
                            # bkgd = "grey" if lit else bg_fog
                    
                        # street border
                        if ch in ("=",):
                            lit = "dark white" if visible else fg_fog

                        if ch in ("x"):
                            lit = "#1e130c" if visible else fg_fog
                        
                        if ch in ("|"):
                            ch, col, _, _ = self.plant[y][x]
                            #level = fog_levels[lit//2] if lit else "darkest " 
                            
                            #lit = "yellow" if visible else fg_fog
                            level = "light "
                            lit = col if visible else fg_fog

                    else:
                        _, color, _, _ = self.walls[y][x]
                        lit = color if visible else fg_fog

                # bkgd = hextup(color, 4,4,4) if lit else bg_fog
                # all said and done -- return by unit block
                try:        
                    yield (x-cx, y-cy, level+lit, ch, bkgd)
                except NameError:
                    yield (x-cx, y-cy, level+lit, ch, None)
        self.lit_reset()