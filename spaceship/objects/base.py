
from typing import Tuple
import math

class Object:
    '''Base object class used in the following subclasses:
        
        Tiles :- WorldTiles, MapTiles

        Units :- NPC's, Monsters, Player
    
        Items :- Armor, Weapons, Usables
    '''
    def __init__(self, x: int, y: int, c: chr, fg: str, bg: str):
        self.x, self.y = x, y
        self.character = c
        self.foreground = fg
        self.background = bg

    def __str__(self):
        return "{}: (x={}, y={}, ch={}, fg={}, bg={}".format(
            self.__class__.__name__, 
            self.x, 
            self.y, 
            self.character,
            self.foreground,
            self.background
        )

    @property
    def position(self):
        return self.x, self.y

    def distance(self, other):
        return math.sqrt(
            math.pow(other.x - self.x, 2) + \
            math.pow(other.y - self.y, 2))


if __name__ == "__main__":
    # unit tests?
    obj = Object(5, 5, 'o', "#ffffff", "#000000")
    print(obj)
    print(obj.position)

    a = Object(0, 0, "a", "#000000", "#ffffff")
    b = Object(9, 9, "b", "#000000", "#ffffff")
    print(a.distance(b))
