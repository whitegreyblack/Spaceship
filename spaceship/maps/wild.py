import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)) + '/../../')
from spaceship.maps.base import Map
from spaceship.maps.utils import blender
from spaceship.maps.charmap import DungeonCharmap as dcm
from spaceship.maps.charmap import WildernessCharmap as wcm
from random import randint, choice

class Desert(Map):
    pass

class Forest(Map):
    chars = {
        ".": ("\"", blender([wcm.GRASS.hexcode[0], wcm.TREES.hexcode[0]])),
        "T": (wcm.TREES.chars, blender(wcm.GRASS.hexcode)),
    }
    chars_block_move =  {"#", "+", "o", "x", "%"}
    def __init__(self, width, height):
        super().__init__(width, height, self.__class__.__name__.lower())
        self.build()
        self.create_tile_map()

    def build(self):
        num_trees = 200
        self.data = [[choice(".") for _ in range(self.width)] for _ in range(self.height)]
                
        for t in range(num_trees):
            self.data[randint(0, self.height-1)][randint(0, self.width-1)] = "T"
            stop_chance = randint(0, num_trees)
            if stop_chance == 0:
                break

class Grassland(Map):
    chars = {
        ".": (wcm.GRASS.chars, blender(wcm.GRASS.hexcode)),
        "T": (wcm.TREES.chars, blender(wcm.GRASS.hexcode)),
    }
    chars_block_move = {"#", "+", "o", "x", "~", "%"}
    def __init__(self, width, height):
        super().__init__(width, height, self.__class__.__name__.lower())
        self.build()
        self.create_tile_map()

    def build(self):
        num_trees = 10
        self.data = [["." for _ in range(self.width)] for _ in range(self.height)]

        # for sure at least 3 trees
        for t in range(3):
             self.data[randint(0, self.height-1)][randint(0, self.width-1)] = "T"

        for t in range(num_trees-3):
            self.data[randint(0, self.height-1)][randint(0, self.width-1)] = "T"
            stop_chance = randint(0, num_trees-t)
            if stop_chance == 0:
                break       

class Hills(Map):
    chars = {
            ".": (wcm.GRASS.chars, blender(wcm.GRASS.hexcode)),
            "~": (wcm.HILLS.chars, blender(wcm.HILLS.hexcode)),
    }
    # Hills has a modified block_move char set due to hills having the same char as water
    #   The modified set has removed the hill char while other maps include it
    chars_block_move =  {"#", "+", "o", "x", "%", "Y", "T"}
    def __init__(self, width, height):
        super().__init__(width, height, self.__class__.__name__.lower())
        self.build()
        self.create_tile_map()

    def build(self):
        num_trees = 10
        vege_chars = (".", "~")
        self.data = [[choice(vege_chars) for _ in range(self.width)] for _ in range(self.height)]

class Plains(Map):
    chars = {
            ".": (".", blender(wcm.PLAIN.hexcode)),
            "T": (wcm.TREES.chars, blender(wcm.TREES.hexcode)),
    }
    def __init__(self, width, height):
        super().__init__(width, height, self.__class__.__name__.lower())
        self.build()
        self.create_tile_map()

    def build(self):
        num_trees = 10
        self.data = [["." for _ in range(self.width)] for _ in range(self.height)]

        # for sure at least 3 trees
        for t in range(3):
             self.data[randint(0, self.height-1)][randint(0, self.width-1)] = "T"

        for t in range(num_trees-3):
            self.data[randint(0, self.height-1)][randint(0, self.width-1)] = "T"
            stop_chance = randint(0, num_trees-t)
            if stop_chance == 0:
                break

class Woods(Map):
    chars = {
            ".": (wcm.GRASS.chars, blender(wcm.GRASS.hexcode)),
            "T": (wcm.TREES.chars, blender(wcm.TREES.hexcode)),            
    }
    def __init__(self, width, height):
        super().__init__(width, height, self.__class__.__name__.lower())
        self.build()
        self.create_tile_map()

    def build(self):
        num_trees = 200
        self.data = [[choice(".") for _ in range(self.width)] for _ in range(self.height)]
                
        for t in range(num_trees):
            self.data[randint(0, self.height-1)][randint(0, self.width-1)] = "T"
            stop_chance = randint(0, num_trees)
            if stop_chance == 0:
                break

class Mountains(Map):
    pass

class Water(Map):
    pass

class Swamps(Map):
    pass

class Wastes(Map):
    pass

terrain = {
    "grass": Grassland,
    "forest": Forest,
    "plains": Plains,
    'woods': Woods,
}

if __name__ == "__main__":
    if len(sys.argv) < 2:

        print("Not enough args")
    elif sys.argv[1] in terrain.keys():
        location = terrain[sys.argv[1]](66, 22)
        print(location)
        print(location.__repr__())
        print(location.__str__())
