import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)) + '/../../')
from base import Map, blender
from charmap import DungeonCharmap as dcm
from charmap import WildernessCharmap as wcm
from random import randint, choice

class Desert(Map):
    pass

class Forest(Map):
    chars = {
        ".": ("\"", blender([wcm.GRASS.hexcode[0], wcm.TREES.hexcode[0]])),
        "T": (wcm.TREES.chars, blender(wcm.GRASS.hexcode)),
    }
    def __init__(self, width, height):
        self.width, self.height = width, height
        self.build()
        print(self.__repr__())

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
    def __init__(self, width, height):
        self.width, self.height = width, height
        self.build()
    
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
    def __init__(self, width, height):
        self.width, self.height = width, height
        self.build()

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
        self.width, self.height = width, height
        self.build()

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
        self.width, self.height = width, height
        self.build()

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
