from imports import *
from colors import color, COLOR, SHIP_COLOR
from random import randint, choice
from constants import SCREEN_HEIGHT as sh
from constants import SCREEN_WIDTH as sw
from maps import hextup, hexone, output, blender, gradient
# TODO: Maybe move map to a new file called map and create a camera class?

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
    
class Map:
    ''' Ray Tracing Implementation based off of Rogue Basin Python Tutorial '''
    mult = [
                [1,  0,  0, -1, -1,  0,  0,  1],
                [0,  1, -1,  0,  0, -1,  1,  0],
                [0,  1,  1,  0,  0, -1, -1,  0],
                [1,  0,  0,  1, -1,  0,  0, -1]
            ]
    wall_colors = blender("#eacda3", "#d6ae7b", 3)
    colors_block = ["#ffc0c0c0", "#ffa0a0a0", "#ff808080", "#ff606060", "#ff404040"]
    grass_colors = blender("#56ab2f", "#a8e063")
    def __init__(self, data):
        self.map_type = "city"
        self.data, self.height, self.width = self.dimensions(data)
        self.light = [[0 for _ in range(self.width)] for _ in range(self.height)]
        self.block = [[self.data[y][x] in ("#", "+",) for x in range(self.width)] for y in range(self.height)]
        #self.stone = forests(self.width, self.height, '.', ["#"])
        self.stone = gradient(self.width, self.height, characters, colorA, colorB)
        #self.grass = forests(self.width, self.height, '|', [";","!"])
        self.grass = gradient(self.width, self.height)
        self.flag = 0
        self.map_display_width = min(self.width, sw-20)
        self.map_display_height = min(self.height, sh-4)

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

    def town(self):
        return self.map_type is "town"


    def lit(self, x, y):
        return self.light[y][x] == self.flag


    def set_lit(self, x, y):
        if 0 <= x < self.width and 0 <= y < self.height:
            self.light[y][x] = self.flag


    #def fov_calc(self, x, y, radius):
    def fov_calc(self, lights):
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
                        self.set_lit(X, Y)
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
        fg_fog = "darkest grey"
        bg_fog = "#ff000000"
        positions = {}

        for unit in units:
            positions[unit.pos()] = unit

        # width should total 80 units
        for x in range(cx, cxe):

            # height should total 24 units
            for y in range(cy, cye):
                town = self.town()
                lit = self.lit(x, y)
                visible = town or lit
                if x == X and y == Y:
                    ch = "@"
                    lit = "white"
                    ## bkgd = "black"

                elif (x, y) in positions.keys() and visible:
                    unit = positions[(x,y)]
                    ch = unit.i
                    lit = unit.c

                else:
                    ch = self.square(x, y)
                    # then try to color according to block type
                    # color the floor
                    if ch in (".", ":",):
                        #_, color, _, _ = self.stone[y][x]
                        #lit = "white" if lit else fog
                        #lit = hexone(color//2) if visible else fg_fog
                        lit = "grey" if visible else fg_fog
                        ## bkgd = "black" if not lit else bg_fog

                    # color some grasses
                    if ch in (",",";","!","`"):
                        ch, col, _, _ = self.grass[y][x]
                        #lit = hextup(color,5,2,5) if visible else fg_fog
                        # bkgd = hextup(color, 5,3,5) if lit else bg_fog
                        lit = col if visible else (fg_fog)
                    # color the water
                    if ch == "~":
                        lit, _ = choice([
                            ("#ff3333ff", "#ff666ff"),
                            ("#ff6666ff", "#ff999ff"),
                            ("#ff9999ff", "#ff999ff")]) if visible else (fg_fog, bg_fog)

                    # color the doors
                    if ch in ("+", "/",):
                            lit = "#ff994C00" if visible else fg_fog
                        # bkgd = "black"i

                    # color the walls
                    if ch == "#":
                        #_, color, _, _ = self.stone[y][x]
                        #lit = hexone(color) if visible else fg_fog
                        lit = choice(self.wall_colors) if visible else fg_fog
                        # bkgd = "grey" if lit else bg_fog
                        #lit = "white" if lit else fog
                    
                    if ch == "%":
                        _, color, _, _ = self.stone[y][x]
                        #lit = hexone(color//2) if lit else fg_fog
                        lit = hextup(color, 3,5,5) if visible else fg_fog
                        # bkgd = "grey" if lit else bg_fog
                   
                    # street border
                    if ch == "=":
                        _, color, _, _ = self.grass[y][x]
                        lit = hextup(color, 3,3,3) if visible else fg_fog
                        # bkgd = hextup(color, 4,4,4) if lit else bg_fog
                # all said and done -- return by unit block        
                yield (x-cx, y-cy, lit, ch)
