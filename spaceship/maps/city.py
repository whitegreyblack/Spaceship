import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)) + '/../../')
from spaceship.maps.base import Map
from charmap import DungeonCharmap as dcm
from charmap import WildernessCharmap as wcm
from base import blender

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
    def __init__(self, map_id, map_img, map_cfg):
        self.map_id = map_id
        self.map_data = map_data

    # Unique to city map
    def parse_img(self, map_image):
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

        lines = []
        colors = set()
        self.spaces = []

        try:
            with Image.open(map_image) as img:
                pixels = img.load()
                w, h = img.size
        except FileNotFoundError:
            raise FileNotFoundError("Cannot find file for stringify: {}".format(map_image))

        for j in range(h):
            line = ""
            for i in range(w):
                # sometimes alpha channel is included so test for all values first
                try:
                    r, g, b, _ = pixels[i, j]
                except ValueError:
                    r, g, b = pixels[i, j]
                if (r, g, b) not in colors:
                    colors.add((r, g, b))
                try:
                    char = stringify_chars[(r, g, b)]
                    if char in (".", ":", ",", "="):
                        self.spaces.append((i, j))
                    line += char
                except KeyError:
                    print((r, g, b))
            lines.append(line)

        # make sure accesses to the set are random
        shuffle(self.spaces)

        return "\n".join(lines)

    # Unique to city map
    def parse_cfg(self, map_cfg):
        units = []

        if not self.spaces:
            raise AttributeError("No world configuration")

        try:
            with open(map_cfg, 'r') as cfg:
                unit = namedtuple("Unit", "race unit char color")
                modifier = ""
                for line in cfg:
                    if line.strip().startswith('#'):
                        pass # these are comments in the file
                    elif line.strip().startswith('['):
                        modifier = line.replace('[', '').replace(']', '').lower().strip()
                    else:
                        job, color, character, number= line.split()
                        if modifier == "":
                            raise ValueError("Configuration file has no race specifier")
                        for _ in range(int(number)):
                            i, j = self.spaces.pop()
                            units.append(
                                Unit(
                                    x=i, 
                                    y=j,
                                    race=modifier,
                                    job=job.lower(),
                                    char=character,
                                    color=color
                                )
                            )
            if debug:
                for u in units:
                    print(u)
        
        except FileNotFoundError:
            print("No unit configuration file found")
        
        except:
            raise
        
        finally:
            return units   

    def fill(self, d, w, h):
        # Should only be called once by init
        def evaluate(char):
            try:
                if self.maptype not in ("dungeon", "city"):
                    t = self.wilderness[self.maptype][char]
                else:
                    t = self.landmarks[char]
            except KeyError:
                raise KeyError("Evaluate Map: {} not in keys".format(char))
            return t
        
        rows = []
        tiles = set()
        tree, ground = None, None
        d = d if isinstance(d, list) else d.split('\n')
        for row in d:
            cols = []
            for col in row:
                chars, hexcodes = evaluate(col)
                light = Light.Unexplored
                block_mov = col in self.block_chars
                block_lit = col not in chars_block_light
                tile = self.tile(
                    choice(chars), 
                    choice(hexcodes), 
                    "black", 
                    light, 
                    block_mov,
                    block_lit, 
                    [])
                tiles.add((tile.char, tile.block_mov, tile.block_lit))
                cols.append(tile)
            rows.append(cols)

        if debug:
            print('\tTiles - {}'.format(tiles))

        return rows      

