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
    def position(self, xy):
        dx, dy = xy
        self.x += dx
        self.y += dy

    def __repr__(self):
        return f"{self.__class__.__name__}: ({self.x}, {self.y})"

    def __add__(self, other):
        try:
            x, y = self.x + other.x, self.y + other.y
        except AttributeError:
            x, y = self.x + other[0], self.y + other[1]
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

class Tile:
    __slots__ = ('character', 'foreground', 'background')
    def __init__(self, character, foreground="white", background="black"):
        self.character = character
        self.foreground = foreground 
        self.background = background
    
    @property
    def color(self):
        return self.foreground, self.background

class Object:
    '''Base object class used in the following subclasses:
        
    Tiles :- WorldTiles, MapTiles

    Units :- NPC's, Monsters, Player

    Items :- Armor, Weapons, Usables

    Implements position and object position interactions

    Position :- Changes constantly so getter/setter

    Graphics :- Doesn't usually change -- for now set as only getter
    '''
    object_id = 0
    
    def __init__(self, x: int, y: int, ch: chr, fg: str, bg: str) -> None:
        Object.object_id += 1
        self.tile = Tile(ch, fg, bg)
        self.local = Point(x, y)
        print(self.local.position)

    def __str__(self) -> str:
        return "{}: (x={}, y={}, ch={}, fg={}, bg={})".format(
            self.__class__.__name__, 
            *self.local.position,
            self.tile.character,
            *self.tile.color)

    def output(self):
        return (*self.local.position, self.tile.char, *self.color())

    def distance(self, other):
        return self.local.distance(other.local)

if __name__ == "__main__":
    # unit tests?
    obj = Object(5, 5, 'o', "#ffffff", "#000000")
    print(obj)
    print(obj.local.position)

    a = Object(0, 0, "a", "#000000", "#ffffff")
    b = Object(9, 9, "b", "#000000", "#ffffff")
    
    print(a.distance(b))
    print(a.local.distance(b.local))
    print(Object.object_id)