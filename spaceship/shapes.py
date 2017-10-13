# graph.py
# includes GRAPH, NODE
# uses graph and node to build an options list
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))+'/../')
from bearlibterminal import terminal as t
from spaceship.tools import bresenhams
from collections import namedtuple
from math import sqrt

class Point:
    '''Geometry Class for a single point'''
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def within(self, x, y, sx=0, sy=0) -> bool:
        return sx <= self.x < x and sy <= self.y < y

    def distance(self, other) -> float:
        return sqrt((self.x-other.x)**2+(self.y-self.x)**2)

    def __repr__(self):
        return "Point: ({}, {})".format(self.x, self.y)

def Tile(Point):
    '''Graphical Class for Point Object'''
    def __init__(self, x, y):
        super().__init__(self, x, y)
        self._char = None

    @property
    def char(self):
        return self._char

    @property.setter
    def char(self, c):
        self._char = c

    def draw(self, x=0, y=0, char='o'):
        term.puts(self.x + x, self.y + y, char)

class Line:
    '''Geometrical class to hold a list of points'''
    def __init__(self, pts):
        self.line = [(x, y) for x, y in pts]

    def endpoints(self):
        return self.line[0], self.line[-1]

class Box:
    def __init__(self, i, x1, y1, x2, y2):
        self.num = i
        self.p1 = Point(x1, y1)
        self.p2 = Point(x1, y1)

    def __repr__(self) -> str:
        return "Box[{}]: ({}, {})".format(self.id, self.p1, self.p2)

    def width(self) -> int:
        return self.p2.x - self.p1.x

    def height(self) -> int:
        return self.p2.y - self.p1.y

    def volume(self) -> int:
        return self.p2.x - self.p1.x * self.p2.y - self.p1.y

    def center(self) -> tuple:
        return (self.p1.x + self.p2.x)//2, (self.p1.y + self.p2.y)//2

    def coordinates(self) -> tuple:
        return (self.p1, (self.p1.x, self.p2.y), (self.p2.x, self.p1.y), self.p2)

    def within(self, x, y, sx=0, sy=0) -> bool:
        return sx <= self.p1.x and self.p2.x < x and sy <= self.p1.y and self.p2.y < y

    def equal(self, other) -> bool:
        return self.p1 == other.p1 and self.p2 == other.p2

    def distance(self, other) -> float:
        return Point(*self.center()).distance(*other.center())

    def intersect(self, other, offset=0) -> bool:
        return (self.p1.x + offset <= other.p2.x and self.p2.x + offset>= other.p1.x and
            self.p1.y + offset <= other.p2.y and self.p2.y + offset >= other.p1.y1)

    def draw(self, other):
        for i in range(self.p1.x, self.p2.x+1):
            for j in range(self.p1.y, self.p2.y+1):
                Point(i, j).draw()

class Graph:
    def __init__(self, rooms):
        self._rooms = rooms


