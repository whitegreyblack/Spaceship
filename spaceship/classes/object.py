from typing import Tuple
from namedlist import namedlist
from re import search
import math

class Color:
    def __init__(self, color):
        if search(r'^#(?:[0-9a-fA-F]{3}){1,2}$', color):
            self.color = color
        else:
            raise ValueError("Hexcode is an invalid color")

class Point:
    __slots__ = ('x', 'y')
    def __init__(self, x, y):
        self.x, self.y = x, y

    @property
    def position(self):
        return self.x, self.y

    @position.setter
    def position(self, point):
        self = point

    def move(self, other):
        try:
            self.x, self.y = self.x + other.x, self.y + other.y
        except AttributeError:
            self.x, self.y = self.x + other[0], self.y + other[1]

    def __repr__(self):
        return f"{self.__class__.__name__}: ({self.x}, {self.y})"

    def __add__(self, other):
        try:
            x, y = self.x + other.x, self.y + other.y
        except AttributeError:
            x, y = self.x + other[0], self.y + other[1]
        finally:
            return Point(x, y)

    def __sub__(self, other):
        try:
            x, y = self.x - other.x, self.y - other.y
        except:
            x, y = self.x - other[0], self.y - other[1]
        finally:
            return Point(x, y)

    def __iadd__(self, other):
        try:
            x, y = self.x + other.x, self.y + other.y
        except AttributeError:
            x, y = self.x + other[0], self.y + other[1]
        finally:
            return Point(x, y)

    def __isub__(self, other):
        try:
            x, y = self.x - other.x, self.y - other.y
        except AttributeError:
            x, y = self.x - other[0], self.y - other[1]
        finally:
            return Point(x, y)

    def __eq__(self, other):
        try:        
            equal = self.x == other.x and self.y == other.y
        except AttributeError:
            equal = self.x == other[0] and self.y == other[1]
        finally:
            return equal

    def distance(self, other):
        return math.sqrt(
            math.pow(other.x - self.x, 2) + math.pow(other.y - self.y, 2))

class Object:
    '''Base object class used in the following subclasses:
    Units :- NPC's, Monsters, Player
    '''
    object_id = 0
    
    def __init__(self, x: int, y: int, ch: chr, fg: str, bg: str) -> None:
        Object.object_id += 1
        self.character = ch
        self.foreground = fg
        self.background = bg
        self.local = Point(x, y)

    def __str__(self) -> str:
        return "{}: (x={}, y={}, ch={}, fg={}, bg={})".format(
            self.__class__.__name__, 
            *self.local.position,
            self.character,
            *self.color)

    @property
    def color(self):
        return self.foreground, self.background

    def output(self):
        return (*self.local.position, self.character, *self.color)

if __name__ == "__main__":
    # unit tests?
    obj = Object(5, 5, 'o', "#ffffff", "#000000")
    print(obj)
    print(obj.local.position)
    print(obj.output())

    a = Object(0, 0, "a", "#000000", "#ffffff")
    b = Object(9, 9, "b", "#000000", "#ffffff")
    print(a.local.distance(b.local))
    print(Object.object_id)