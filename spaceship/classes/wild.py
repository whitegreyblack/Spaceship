import os
import sys
from .map import Map
from .utils import blender
from collections import namedtuple
from random import randint, choice, choices

charmap = namedtuple("Charmap", "chars hexcode")
class WildernessCharmap:
    GRASS=charmap([",", ";", "`","\'", "\""], ("#56ab2f", "#a8e063"))
    PLAIN=charmap([".", "\"", ","], ("#F3E347", "#56ab2f"))
    TREES=charmap(["Y", "T", "f"], ("#994C00", "#994C00"))
    HILLS=charmap(["~"], ("#994C00", "#9A8478"))
wcm = WildernessCharmap

class Desert(Map):
    chars = {
            "~": (["~"], blender(["#F0AC82", "#C3B091"])),
    }
    # Hills has a modified block_move char set due to hills having the same char as water
    #   The modified set has removed the hill char while other maps include it
    chars_block_move =  {"#", "+", "o", "x", "%", "Y", "T"}
    def __init__(self, width=66, height=22, generate=False):
        super().__init__(width, height, "Wild")
        self.build()
        self.create_tile_map()
        
        if generate:
            self.generate_units()

    def build(self):
        self.spaces = []
        self.data = []
        for y in range(self.height):
            col = []
            for x in range(self.width):
                col.append("~")
                self.spaces.append((x, y))
            self.data.append(col)

        def build_oasis():
            '''Chance that an oasis will pop up in the desert'''
            # we use a class variable to keep track of the percentage
            # Desert.chance_for_oasis = 100?
            ...
        def build_monster_nest():
            '''Chance that a monster nest will be generated during map gen'''
            # only monsters that will be generated in a desert environment will be
            # sandworm, orc dune walker, basically desert creatures
            # if oasis is generated then creature list really grows 
            ...

class Forest(Map):
    """
    Args:
        var chars
        var chars_block_move

    Functions:
        build()
    """
    chars = {
        # ".": ("\"", blender([wcm.GRASS.hexcode[0], wcm.TREES.hexcode[0]])),
        ".": ("\"", ("#5D9645",)),
        "T": (wcm.TREES.chars, blender(wcm.GRASS.hexcode)),
    }
    chars_block_move =  {"#", "+", "o", "x", "%"}
    def __init__(self, width=66, height=22, generate=False):
        super().__init__(width, height, "Wild")
        self.build()
        self.create_tile_map()
        if generate:
            self.generate_units()

    def build(self):
        num_trees = 200
        self.spaces = []
        self.data = []
        for y in range(self.height):
            col = []
            for x in range(self.width):
                if num_trees:
                    char = choices(population=[".", "T"], weights=[.9, .1], k=1)[0]
                    if char == "T":
                        num_trees -= 1
                else:
                    char = "."
                if char == ".":
                    self.spaces.append((x, y))
                col.append(char)
            self.data.append(col)
                
        # self.data = [[choice(".") for _ in range(self.width)] for _ in range(self.height)]
                
        # for t in range(num_trees):
        #     self.data[randint(0, self.height-1)][randint(0, self.width-1)] = "T"
        #     stop_chance = randint(0, num_trees)
        #     if stop_chance == 0:
        #         break

class Grassland(Map):
    '''build()'''
    chars = {
        ".": (wcm.GRASS.chars, blender(wcm.GRASS.hexcode)),
        "T": (wcm.TREES.chars, blender(wcm.GRASS.hexcode)),
    }
    chars_block_move = {"#", "+", "o", "x", "~", "%"}
    def __init__(self, width=66, height=22, generate=False):
        super().__init__(width, height, "Wild")
        self.build()
        self.create_tile_map()
        if generate:
            self.generate_units()

    def build(self):
        num_trees = 10
        self.data = [["." for _ in range(self.width)] for _ in range(self.height)]

        # for sure at least 3 trees
        for t in range(3):
             self.data[randint(0, self.height-1)][randint(0, self.width - 1)] = "T"

        for t in range(num_trees - 3):
            self.data[randint(0, self.height - 1)][randint(0, self.width - 1)] = "T"
            stop_chance = randint(0, num_trees - t)
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
    def __init__(self, width=66, height=22, generate=False):
        super().__init__(width, height, "Wild")
        self.build()
        self.create_tile_map()
        if generate:
            self.generate_units()

    def build(self):
        num_trees = 10
        vege_chars = (".", "~")
        self.spaces = []
        self.data = []
        for y in range(self.height):
            col = []
            for x in range(self.width):
                col.append(choice(vege_chars))
                self.spaces.append((x, y))
            self.data.append(col)

        # self.data = [[choice(vege_chars) for _ in range(self.width)] for _ in range(self.height)]
        # self.spaces = [(x, y) for y in range(self.height) for x in range(self.width)]

class Plains(Map):
    chars = {
            ".": (".", blender(wcm.PLAIN.hexcode)),
            "T": (wcm.TREES.chars, blender(wcm.TREES.hexcode)),
    }
    def __init__(self, width=66, height=22, generate=False):
        super().__init__(width, height, "Wild")
        self.build()
        self.create_tile_map()
        if generate:
            self.generate_units()

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

        self.spaces = [(x, y) for y in range(self.height) for x in range(self.width) if self.data[y][x] == "."]

class Woods(Map):
    chars = {
            ".": (wcm.GRASS.chars, blender(wcm.GRASS.hexcode)),
            "T": (wcm.TREES.chars, blender(wcm.TREES.hexcode)),            
    }
    def __init__(self, width=66, height=22, generate=False):
        super().__init__(width, height, "Wild")
        self.build()
        self.create_tile_map()
        if generate:
            self.generate_units()

    def build(self):
        num_trees = 200
        self.data = [[choice(".") for _ in range(self.width)] for _ in range(self.height)]
                
        for t in range(num_trees):
            self.data[randint(0, self.height-1)][randint(0, self.width-1)] = "T"
            stop_chance = randint(0, num_trees)
            if stop_chance == 0:
                break
        
        self.spaces = [(x, y) for y in range(self.height) for x in range(self.width) if self.data[y][x] == "."]

class Mountains(Map):
    pass

class Water(Map):
    pass

class Swamps(Map):
    pass

class Wastes(Map):
    pass

wilderness = {
    "grass": Grassland,
    "forest": Forest,
    "plains": Plains,
    'dark woods': Woods,
    'desert': Desert,
    'hills': Hills,
}

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Not enough args")
    elif sys.argv[1] in terrain.keys():
        location = terrain[sys.argv[1]](66, 22)
        print(location.__repr__())
        print(location.__str__())
