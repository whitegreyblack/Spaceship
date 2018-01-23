from typing import Tuple
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

class Tile:
    def __init__(self, ch, fg, bg):
        self.character = ch
        self.foreground = fg
        self.background = bg

    def draw(self):
        return self.character, self.foreground, self.background

class WorldTile(Tile):
    def __init__(self, ch, fg, bg, land, enterable):
        super().__init__(ch, fg, bg)
        self.land = land
        self.enterable = enterable

    def draw(self):
        return (*super().draw(), self.land, self.enterable)
    
class MapTile(Tile):
    def __init__(self, ch, fg, block, light):
        super().__init__(ch, fg, bg)
        self.block = block
        self.light = light

    def draw(self):
        return (*super().draw(), self.block, self.light)

class Object(Tile):
    '''Base object class used in the following subclasses:
        
    Tiles :- WorldTiles, MapTiles

    Units :- NPC's, Monsters, Player

    Items :- Armor, Weapons, Usables

    Implements position and object position interactions

    Position :- Changes constantly so getter/setter

    Graphics :- Doesn't usually change -- for now set as only getter
    '''
    object_id = 0
    
    def __init__(self, x: int, y: int, ch: chr, fg: str, bg: str):
        super().__init__(ch, fg, bg)
        self.x, self.y = x, y
        Object.object_id += 1

    def __str__(self):
        return "{}: (x={}, y={}, ch={}, fg={}, bg={})".format(
            self.__class__.__name__, 
            self.x, 
            self.y, 
            self.character,
            self.foreground,
            self.background
        )

    @property
    def position(self) -> Tuple[int, int]:
        '''returns local position within a non-global map'''
        return self.x, self.y

    @position.setter
    def position(self, position: Tuple[int, int]) -> None:
        '''sets local position given a tuple(x,y)'''
        self.x, self.y = position

    def distance(self, other):
        return math.sqrt(
            math.pow(other.x - self.x, 2) + \
            math.pow(other.y - self.y, 2))

    def output(self):
        return (*super().draw(), self.x, self.y)

if __name__ == "__main__":
    # unit tests?
    obj = Object(5, 5, 'o', "#ffffff", "#000000")
    print(obj)
    print(obj.position)

    a = Object(0, 0, "a", "#000000", "#ffffff")
    b = Object(9, 9, "b", "#000000", "#ffffff")
    print(a.distance(b))

    print(Object.object_id)