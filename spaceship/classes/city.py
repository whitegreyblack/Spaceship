from random import shuffle, choice, randint
from collections import namedtuple
from PIL import Image
from collections import namedtuple
from .map import Map
from .utils import blender
from .unit import Unit
from .neutrals import neutrals
from ..strings import IMG_PATH
# cities.py
'''
Shadowbarrow
X==XX  XooXX oXXo
=+===  o+ooo X+XX
X==XX  oooXX XXXo
XX=XX  XoXXX =X==

Renmar:
XXXX=
==+==
X==XX

Westwatch:
X==
=+=
X=X

Components

Tree -> animatable -> treent
    Leaves -> weavable, burnable
    Branches -> burnable, sharpenable
    Trunk -> burnable, craftable, splittable
    Roots -> burnable
Stone -> animatable -> stone golem
      -> Heatable -> gives off heat
      -> throwable

Mud -> animatable -> mud golem
Water -> animatable -> Water Elemental
Fire -> animatable -> Fire Lord
Air -> animatable -> Wind Zephyr
Corpse -> animatable -> Zombie

# Wood
# Stone
# Minerals/Jewels
# Metals
# Cloth
# Leather
# 
'''
charmap = namedtuple("Charmap", "chars hexcode")
class DungeonCharmap:
    # GRASS=charmap([",", ";"], ("#56ab2f", "#a8e063"))
    GRASS=charmap([",", ";"], ("#008800", "#008800"))
    HOUSE=charmap(["="], ("#ffffff", "#ffffff"))
    TILES=charmap(["."], ("#C0C0C0", "#C0C0C0"))
    # TILES=charmap(["."], ("#404040", "#404040"))
    WALLS=charmap(["#"], ("#444444", "#656565"))
    # WATER=charmap(["~"], ("#43C6AC", "#191654"))
    WATER=charmap(["~"], ("#191654", "#191654"))
    # WATER=charmap(["~"], ("#43C6AC", "#43C6AC"))

    DOORS=charmap(["+"], ("#994C00", "#994C00"))
    # PLANT=charmap(["|"], ("#F3E347", "#24FE41"))
    PLANT=charmap(["'"], ("#ffc90e", "#ffc90e"))

    LAMPS=charmap(["o"], ("#ffffff", "#ffffff"))
    BRICK=charmap(["%"], ("#a73737", "#7a2828"))
    # ROADS=charmap([":"], ("#808080", "#994C00"))
    ROADS=charmap([":"], ("#994C00", "#994C00"))
    POSTS=charmap(["x"], ("#9a8478", "#9a8478"))
    BLOCK=charmap(["#", "+", "o", "x"],("#000000", "#ffffff"))
    LTHAN=charmap(["<"], ("#c0c0c0", "#c0c0c0"))
    GTHAN=charmap([">"], ("#c0c0c0", "#c0c0c0"))
    TRAPS=charmap(["^"], ("#c0c0c0", "#c0c0c0"))

dcm = DungeonCharmap

class City(Map):
    chars = {
        ".": (dcm.TILES.chars, blender(dcm.TILES.hexcode)),
        ",": (dcm.GRASS.chars, blender(dcm.GRASS.hexcode)),
        "#": (dcm.WALLS.chars, blender(dcm.WALLS.hexcode)),
        "~": (dcm.WATER.chars, blender(dcm.WATER.hexcode)),
        "+": (dcm.DOORS.chars, blender(dcm.DOORS.hexcode)),
        "x": (dcm.POSTS.chars, blender(dcm.POSTS.hexcode)), 
        "|": (dcm.PLANT.chars, blender(dcm.PLANT.hexcode)),
        "o": (dcm.LAMPS.chars, blender(dcm.LAMPS.hexcode)),
        ":": (dcm.ROADS.chars, blender(dcm.ROADS.hexcode)),
        "=": (dcm.HOUSE.chars, blender(dcm.HOUSE.hexcode)),
        " ": (' ', '#000000'),
        "%": (dcm.WALLS.chars, blender(dcm.WALLS.hexcode)),
        "^": (dcm.WALLS.chars, blender(dcm.WALLS.hexcode)),
        "<": (dcm.LTHAN.chars, blender(dcm.LTHAN.hexcode)),
        ">": (dcm.GTHAN.chars, blender(dcm.GTHAN.hexcode)),
        "^": (dcm.TRAPS.chars, blender(dcm.TRAPS.hexcode)),
        "S": (["."], blender(dcm.TILES.hexcode)),
        "B": (["."], blender(dcm.TILES.hexcode)),
        "I": (["."], blender(dcm.TILES.hexcode)),
        "G": (["."], blender(dcm.TILES.hexcode)),
    }

    chars_block_move = {"#", "+", "o", "x", "~", "%", "Y", "T",}

    def __init__(self, map_id, map_img, map_cfg):
        self.map_id = map_id
        self.map_img = map_img
        self.map_cfg = map_cfg
        width, height = self.parse_img() # <== creates initial data map
        self.parse_cfg()

        super().__init__(width, height, self.__class__.__name__)

        self.create_tile_map()
        # print(repr(self))

    # def __repr__(self):
    #     return "{}:\n{}\n{}".format(
    #         self.map_id,
    #         self.print_map(),
    #         self.print_units())

    def __str__(self):
        return "{}:\n{}\n{}".format(
            self.map_id,
            self.print_map(),
            self.print_units())

    # Unique to city map
    def parse_img(self):
        """Takes in a file location string and a bool for debug
        to determine output. Sister function to asciify. Uses 
        only keyboard accessible characters in the map."""
        stringify_chars = { 
            (0, 0, 0): "#",
            (136, 0, 21): "%",
            (255, 242, 0): "=",
            (34, 177, 76): ",",
            (185, 122, 87): "+",
            (127, 127, 127): ".",
            (112, 146, 190): "=",   
            (153, 217, 234): "=",
            (195, 195, 195): ":",
            (241, 203, 88): "|",
            (255, 201, 14): "|",
            (0, 162, 232): "~",
            (98, 81, 43): "x",
            (239, 228, 176): ",",
            (63, 72, 204): "S",
            (255, 255, 255): "B",
            (255, 127, 39): "I",
            (237, 28, 36): "G",
        }

        self.data = []
        self.spaces = []
        self.spaces_bishop = []
        self.spaces_guards = []
        self.spaces_villagers = []
        self.spaces_innkeeper = []
        self.spaces_shopkeeper = []
        self.unit_spaces = {
            "B": self.spaces_bishop,
            "G": self.spaces_guards,
            "V": self.spaces_villagers,
            "I": self.spaces_innkeeper,
            "S": self.spaces_shopkeeper,
        }

        try:
            with Image.open(self.map_img) as img:
                pixels = img.load()
                w, h = img.size
        except FileNotFoundError:
            with Image.open(IMG_PATH + 'sample.png') as img:
                pixels = img.load()
                w, h = img.size

        for j in range(h):
            line = ""

            for i in range(w):
                try:
                    r, g, b, _ = pixels[i, j]
                    
                except ValueError:
                    r, g, b = pixels[i, j]

                try:
                    char = stringify_chars[(r, g, b)]

                    if char in self.unit_spaces.keys():
                        self.unit_spaces[char].append((i, j))
                        # revert the char to its original space
                        char = "."

                    elif char in (".", ":", ",", "="):
                        if 0 <= i < w and 0 <= j < h:
                            self.spaces.append((i, j))

                    line += char

                except KeyError:
                    print((r, g, b))

            self.data.append(line)

        # make sure accesses to the set are random
        shuffle(self.spaces)
        return w, h

    # Unique to city map
    def parse_cfg(self):
        if not self.spaces:
            raise AttributeError("No world configuration")

        self.stats = "{}: Unit List\n".format(self.map_id)

        try:
            with open(self.map_cfg, 'r') as cfg:
                modifier = ""

                for line in cfg:
                    if line.strip().startswith('#'):
                        pass # these are comments in the file

                    elif line.strip().startswith('['):
                        modifier = line.replace('[', '').replace(']', '')
                        modifier = modifier.lower().strip()

                    else:
                        job, color, character, number = line.split()
                        self.stats += "{}: {}\n".format(job, number)

                        if modifier == "":
                            e="Configuration file has no race specifier"
                            raise ValueError(e)

                        if job.lower() in neutrals.keys():
                            for _ in range(int(number)):
                                try:
                                    spaces=self.unit_spaces[character] \
                                        if self.unit_spaces[character] \
                                        else self.spaces

                                except KeyError:
                                    spaces = self.spaces

                                else:
                                    i, j = choice(spaces)

                                self.units_add([neutrals[job.lower()](
                                    x=i, 
                                    y=j,
                                    race=modifier,
                                    job=job.lower(),
                                    ch=character,
                                    fg=color,
                                    spaces=self.unit_spaces[character] 
                                        if self.unit_spaces[character] 
                                        else self.spaces)])

                        else:
                            for _ in range(int(number)):
                                i, j = self.spaces.pop()
                                self.units.append(Unit(
                                    x=i, 
                                    y=j,
                                    ch=character,
                                    fg=color))
                                                                        
        except FileNotFoundError:
            # not explicitely needed -- can just pass instead of printing
            print("No unit configuration file found")
        
        except:
            # any other error should be raised
            raise

    def print_map(self):
        if hasattr(self, 'data'):
            return "\n".join(self.data)

    def print_units(self):
        if hasattr(self, 'stats'):
            return self.stats

if __name__ == "__main__":
    img = "./spaceship/assets/maps/shadowbarrow.png"
    cfg = "./spaceship/assets/maps/shadowbarrow.cfg"
    test = City("shadowbarrow", img, cfg, 80, 25)
    print(test)