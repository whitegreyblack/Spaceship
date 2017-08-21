from imports import *
from colors import COLOR, color, SHIP_COLOR

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


class Plane(object):
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


class Map(Plane):
    def __init__(self, x, y):
        super(Rectangle, self).__init__(x, y)
        self.points = [Point(x, y) for x in self.x for y in self.y]

    def getPoint(self, x, y):
        return self.points[x][y]

    def setPoint(self, x, y, v):
        try:
            self.poinst[x][y] = v
        except BaseException:
            print('Unable to set value to point')


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
