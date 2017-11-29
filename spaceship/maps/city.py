import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)) + '/../../')
from spaceship.maps.base import Map, blender
from PIL import Image
from collections import namedtuple
from spaceship.maps.charmap import DungeonCharmap as dcm
from spaceship.maps.charmap import WildernessCharmap as wcm
from random import shuffle, choice, randint
from spaceship.units.unit import Unit
from spaceship.units.neutrals import Shopkeeper, Innkeeper, Bishop, Soldier

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
    }
    def __init__(self, map_id, map_img, map_cfg, width, height):
        super().__init__(width, height, self.__class__.__name__.lower())
        self.map_id = map_id
        self.map_img = map_img
        self.map_cfg = map_cfg
        self.parse_img() # <== creates initial data map
        self.parse_cfg()
        self.create_tile_map()
        self.relationship = 100

    def __repr__(self):
        return "{}:\n{}\n{}".format(
            self.map_id,
            self.print_map(),
            self.print_units())

    def __str__(self):
        return "{}:{} ({}, {})".format(
            self.__class__.__name__,
            self.map_id,
            self.width,
            self.height)

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
            (255, 255, 255): ".",
            (195, 195, 195): ":",
            (241, 203, 88): "|",
            (255, 201, 14): "|",
            (0, 162, 232): "~",
            (98, 81, 43): "x",
            (239, 228, 176): ",",
        }

        self.data = []
        self.spaces = []

        try:
            with Image.open(self.map_img) as img:
                pixels = img.load()
                w, h = img.size
        except FileNotFoundError:
            raise FileNotFoundError("Cannot find file for stringify: {}".format(self.map_img))

        for j in range(h):
            line = ""
            for i in range(w):
                # sometimes alpha channel is included so test for all values first
                try:
                    r, g, b, _ = pixels[i, j]
                except ValueError:
                    r, g, b = pixels[i, j]
                try:
                    char = stringify_chars[(r, g, b)]
                    if char in (".", ":", ",", "="):
                        self.spaces.append((i, j))
                    line += char
                except KeyError:
                    print((r, g, b))
            self.data.append(line)

        # make sure accesses to the set are random
        shuffle(self.spaces)

    # Unique to city map
    def parse_cfg(self):
        if not self.spaces:
            raise AttributeError("No world configuration")

        jobs = {
            "bishop": Bishop,
            "innkeeper": Innkeeper,
            "shopkeeper": Shopkeeper,
            "soldier": Soldier,
        }
        self.stats = "{}: Unit List\n".format(self.map_id)
        try:
            with open(self.map_cfg, 'r') as cfg:
                modifier = ""
                for line in cfg:
                    if line.strip().startswith('#'):
                        pass # these are comments in the file
                    elif line.strip().startswith('['):
                        modifier = line.replace('[', '').replace(']', '').lower().strip()
                    else:
                        job, color, character, number = line.split()
                        self.stats += "{}: {}\n".format(job, number)

                        if modifier == "":
                            raise ValueError("Configuration file has no race specifier")
                        if job.lower() in jobs.keys():
                            for _ in range(int(number)):
                                i, j = self.spaces[randint(0, len(self.spaces)-1)]
                                self.units.append(jobs[job.lower()](
                                            x=i, 
                                            y=j,
                                            race=modifier,
                                            job=job.lower(),
                                            char=character,
                                            color=color))
                        else:
                            for _ in range(int(number)):
                                i, j = self.spaces.pop()
                                self.units.append(Unit(
                                            x=i, 
                                            y=j,
                                            race=modifier,
                                            job=job.lower(),
                                            char=character,
                                            color=color))
        except FileNotFoundError:
            # not explicitely needed
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
    img = "./assets/maps/shadowbarrow.png"
    cfg = "./assets/maps/shadowbarrow.cfg"
    test = City("shadowbarrow", img, cfg, 80, 25)
    print(test)
    print(repr(test))