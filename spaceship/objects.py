from imports import *
from colors import color, COLOR, SHIP_COLOR
from random import randint, choice
from constants import SCREEN_HEIGHT as sh
from constants import SCREEN_WIDTH as sw
from maps import gradient, hextup, hexone, output
# TODO: Maybe move map to a new file called map and create a camera class?

class TextBox:
    def __init__(self, string):
        self.string = string

class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __repr__(self):
        return "{}({},{})".format(
            self.__class__.__name__, self.x, self.y)


class Plane:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.size = x * y

    def getter(self):
        return self.x, self.y, self.size

    def update(self, x, y):
        self.x = x
        self.y = y
        self.size = x * y

    def __repr__(self):
        return "{}({},{},{})".format(
            self.__class__.__name__, self.x, self.y, self.size)

'''
class Map(Plane):
    def __init__(self, x, y):
        super(Map, self).__init__(x, y)
        self.points = [Point(x, y) for x in self.x for y in self.y]

    def getPoint(self, x, y):
        return self.points[x][y]

    def setPoint(self, x, y, v):
        try:
            self.points[x][y] = v
        except BaseException:
            print('Unable to set value to point')
'''

class Rectangle(Plane):
    def __init__(self, x, y, dx, dy):
        super(Rectangle, self).__init__(dx, dy)
        self.tl = Point(x, y)
        self.tr = Point(x + dx - 1, y)
        self.bl = Point(x, y + dy - 1)
        self.br = Point(x + dx - 1, y + dy - 1)

    def pts(self):
        return self.tl, self.tr, self.bl, self.br

    def ctr(self):
        return (self.tl.x + self.br.x) / 2, (self.tl.y + self.br.y) / 2

    def cross(self, other):
        return (self.tl.x <= other.br.x and self.br.x <= other.tl.x and
                self.tl.y <= other.br.y and self.br.y <= other.tl.y)

    def __repr__(self):
        return "{}({},{},{})\n({},{})\n({},{})".format(
            self.__class__.__name__, self.x, self.y, self.size,
            self.tl, self.tr, self.bl, self.br)


class Grid:
    def __init__(self, dx, dy, v):
        self.mx = dx
        self.my = dy
        self.walkable = set()
        self.map = [[v for y in range(dy)] for x in range(dx)]

    def __repr__(self):
        return "{}({},{},{})".format(
            self.__class__.__name__, self.mx, self.my, type(self.map[0][0]))

'''
class Tile(Point):
    def __init__(self, x, y, blocked, block_sight):
        super(Tile, self).__init__(x, y)
        self.blocked = blocked
        self.explored = False
        self.block_sight = block_sigh if block_sight else blocked

class GameObject(Point):
    def __init__(self, x, y, char, color=None):
        self.x = x
        self.y = y
        self.char = char
        self.color = color if color else Color(0, 0, 0)

    def __repr__(self):
        return "{}({},{},{},{}".format(self.__class__.__name__,
                                       self.x, self.y, self.char, self.color)

class ImmovableObject(GameObject):
    def __init__(self, x, y, char, color=None):
        super(ImmovableObject, self).__init__(x, y, char, color)


class MovableObject(GameObject):
    def __init__(self, x, y, char, color=None):
        super(MovableObject, self).__init__(x, y, char, color)

    def move(self, dx, dy, tile):
        if tile.open:
            self.x += dx
            self.y += dy
'''

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

class Tile:
    def __init__(self, blocked, sight=None):
        self.blocked = blocked
        self.sight = blocked if sight is None else sight

class Map:
    ''' Ray Tracing Implementation based off of Rogue Basin Python Tutorial '''
    mult = [
                [1,  0,  0, -1, -1,  0,  0,  1],
                [0,  1, -1,  0,  0, -1,  1,  0],
                [0,  1,  1,  0,  0, -1, -1,  0],
                [1,  0,  0,  1, -1,  0,  0, -1]
            ]
    colors_block = ["#ffc0c0c0", "#ffa0a0a0", "#ff808080", "#ff606060", "#ff404040"]
    def __init__(self, data):
        self.data, self.height, self.width = self.dimensions(data)
        self.light = [[0 for _ in range(self.width)] for _ in range(self.height)]
        self.block = [[self.data[y][x] in ("#", "+",) for x in range(self.width)] for y in range(self.height)]
        self.stone = gradient(self.width, self.height, '.', ["#"])
        output(self.stone)
        self.grass = gradient(self.width, self.height, '.', [",",";",])
        output(self.grass)
        print(self.height, self.width)
        self.flag = 0

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


    def lit(self, x, y):
        return self.light[y][x] == self.flag


    def set_lit(self, x, y):
        if 0 <= x < self.width and 0 <= y < self.height:
            self.light[y][x] = self.flag


    def fov_calc(self, x, y, radius):
        self.flag += 1
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
            hs = s//2
            if p < hs:
                return 0
            elif p >= m - hs:
                return m - s
            else:
                return p - hs

        cx = scroll(X, self.width if self.width <= 80 else 80, self.width)
        cy = scroll(Y, self.height if self.height <= 24 else 24, self.height)
        fog = "#ff404040"

        positions = {}
        for unit in units:
            positions[unit.pos()] = unit
        # width should total 80 units
        for x in range(cx, cx+(80 if self.width > 80 else self.width)):
            # height should total 24 units
            for y in range(cy+(24 if self.height > 24 else self.height)):
                lit = self.lit(x, y)
                if x == X and y == Y:
                    ch = "@"
                    lit = "white"
                elif (x, y) in positions.keys() and lit:
                    unit = positions[(x,y)]
                    ch = unit.i
                    lit = unit.c
                else:
                    ch = self.square(x, y)
                    if ch == ".":
                        #_, color, _, _ = self.stone[y][x]
                        lit = "white" if lit else fog
                        #lit = element.hexone(color) if lit else fog
                    if ch in (",",";","!",):
                        ch, color, _, _ = self.grass[y][x]
                        lit = hextup(color,5,2,5) if lit else fog
                    if ch == "~":
                        lit = choice(["#ff6666ff", "#ff3333ff", "#ff9999ff"]) if lit else fog
                    if ch in ("+", "/",):
                        lit = "#ff994C00" if lit else fog
                    if ch == "#":
                        #_, color, _, _ = self.stone[y][x]
                        #lit = element.hexone(color) if lit else fog
                        lit = "white" if lit else fog
                yield (x-cx, y-cy, lit, ch)
