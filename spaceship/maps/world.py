import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)) + '/../../')
from spaceship.maps.base import Map
from spaceship.maps.utils import blender
from PIL import Image
from collections import namedtuple
from spaceship.maps.charmap import DungeonCharmap as dcm
from spaceship.maps.charmap import WildernessCharmap as wcm
from spaceship.maps.charmap import WorldCharmap as ccm
from random import shuffle, choice, randint
from spaceship.maps.utils import splitter

class World(Map):
    chars = {
        '&': ('city', ("#FF8844",)),
        '#': ('fort', ("#FF00FF",)),
        '+': ('town', ("#00fF00",)),
        'o': ('hold', ("#FF0000",)),
        '^': ('mountain', ("#FFFFFF",)),
        '~': ('hills', ("#826644",)),
        'T': ('forest', ("#568203",)),
        '.': ('plains', ("#FFBF00",)),
        '"': ('grassland', 
        '*': ('dungeon',
        '=': ('ocean',
        
    }

    class WorldTile(Map.Tile):
        def __init__(self, char, color, block_mov, block_lit, tile_type, tile_name=None):
            '''Inherits from Map.Tile to create a tile specific for a world map'''
            super().__init__(char, color, block_mov, block_lit)
            self.ttype = ttype
            if self.name:
                self.name = name

    def __init__(self, map_img_path):
        self.map_img_path = map_img_path
        self.parse_img()
        self.create_map_tile()
        super().__init__(self.width, self.height, self.__class__.__name__)
        

    def __repr__(self):
        return """\
    {}:
    [Locations]:
        {}""".format(self.__class__.__name__,
        "\n\t".join([str(x) for x in self.locations])
        )

    def __str__(self):
        return "[{}] Locations: {}".format(
            self.name, 
            len(self.locations))

    def parse_img(self):
        """Takes in a file location string to create map object"""
        stringify_chars = {
            (200, 191, 231): "&",
            (153, 217, 234): "#",
            (163, 73, 164): "&",
            (237, 28, 36): "+",
            (136, 0, 21): "o",
            (255, 255, 255): "^",
            (195, 195, 195): "A",
            (127, 127, 127): "A",
            (185, 122, 87): "~",
            (181, 230, 29): "T",
            (34, 177, 76): "T",
            (255, 201, 14): ".",
            (255, 127, 39): ".",
            (255, 242, 0): "X",
            (255, 174, 201): "%",
            (112, 146, 190): "~",
            (63, 72, 204): "-",
            (0, 162, 232): "=",
            (0, 0, 0): "*",
        }  

        self.map_string = []
        self.locations = []

        try:
            with Image.open(self.map_img_path) as img:
                pixels = img.load()
                self.width, self.height = img.size
        except FileNotFoundError:
            raise FileNotFoundError("Cannot find file for stringify: {}".format(self.map_img_path))

        for j in range(self.height):
            line = ""
            for i in range(self.width):
                # sometimes alpha channel is included so test for all values first
                try:
                    r, g, b, _ = pixels[i, j]
                except ValueError:
                    r, g, b = pixels[i, j]
                try:
                    char = stringify_chars[(r, g, b)]
                    if char in ("&", "o", "+", "#"):
                        self.locations.append((i, j))
                    line += char
                except KeyError:
                    print((r, g, b))
            self.map_string.append(line)

    def create_tile_map(self):
        if not hasattr(self, 'map_string'):
            raise AttributeError("No self.data")
        if not hasattr(self, 'chars'):
            raise AttributeError("No self.chars")
       
        self.map_tile = []
        for j, row in enumerate(self.map_string):
            cols = []
            for i, char in enumerate(row):
                try:
                    tile_type, hexcodes = self.chars[char]
                except KeyError:
                    raise KeyError("Create Tile Map: '{}' not in keys".format(char))

                hexcode = hoice(hexcodes) if len(hexcodes) > 1 else hexcodes,
                block_mov = char in self.chars_block_move
                block_lit = char in self.chars_block_light
                tile_name = cities[(i,j)] if char in ("&", "o", "+", "#") else None
                
                tile = self.WorldTile(
                    char=char,
                    color=hexcode,
                    block_mov=block_mov,
                    block_lit=block_mov, 
                    tile_type=tile_type,
                    tile_name=tile_name)
                    
                cols.append(tile)
            rows.append(cols)

    def save_map_check(self):
        folder_name = "world_map"
        maps_path = "./{}/".format(folder_name)
        if not os.path.isdir(folder_name):
            print("Picturfy folder does not exist -- Creating './{}'".format(
                folder_name))
            os.makedirs(folder_name)

    def save_map_tile(self):
        self.save_map_check()
        file_name = "world_map.png"
        for j, row in enumerate(self.map_tile):
            for i, tile in enumerate(row):
                pass
                
    def save_map_string(self):
        self.save_map_check()
        file_name = "world_map.txt"
        with open("./world_map/" + file_name, 'w') as text:
            for row in self.map_string:
                text.write("".join(row))

if __name__ == "__main__":
    w = World(map_img_path="./assets/worldmap.png")
    # for j in w.data:
    #     print(j)
    # print(w.__repr__())
    # w.create_tile_map()
    w.save_map_string()
    