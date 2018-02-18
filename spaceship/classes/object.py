from typing import Tuple
from namedlist import namedlist
from .point import Point
from re import search
import math

class Color:
    def __init__(self, color):
        if search(r'^#(?:[0-9a-fA-F]{3}){1,2}$', color):
            self.color = color
        else:
            raise ValueError("Hexcode is an invalid color")

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