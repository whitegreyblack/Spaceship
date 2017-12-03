import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)) + '/../../')
from spaceship.maps.base import Map
from spaceship.maps.utils import blender
from PIL import Image, ImageDraw
from collections import namedtuple
from spaceship.maps.charmap import DungeonCharmap as dcm
from spaceship.maps.charmap import WildernessCharmap as wcm
from spaceship.maps.charmap import WorldCharmap as ccm
from random import shuffle, choice, randint
from spaceship.maps.utils import splitter
from spaceship.tools import toInt

class World(Map):
    class WorldTile(Map.Tile):
        def __init__(self, char, color, block_mov, block_lit, tile_type, tile_name=None):
            '''Inherits from Map.Tile to create a tile specific for a world map'''
            super().__init__(char, color, block_mov, block_lit)
            self.tile_type = tile_type
            if tile_name:
                self.name = tile_name

        def __repr__(self):
            return self.char

        def __str__(self):
            return self.char

    def __init__(self, map_img_path):
        self.tilemap = map_img_path
        # super().__init__(self.width, self.height, self.__class__.__name__)

    def __repr__(self):
      return "{}: ({}, {})".format(
        self.__class__.__name__,
        self.width, self.height)

    def __str__(self):
        return "\n".join("".join(tile.char for tile in row) for row in self.tilemap)

    @property
    def tilemap(self):
        return self.__tile_map

    @tilemap.setter
    def tilemap(self, path):
        """Takes in a file location string to create map object"""
        chars = {
            (200, 191, 231): ("city", "&", ("#FF8844",)),
            (153, 217, 234): ("hold", "#", ("#FF00FF",)),
            (163, 73, 164): ("city", "&", ("#FFFF00",)),
            (237, 28, 36): ("town", "+", ("#00fF00",)),
            (136, 0, 21): ("fort", "o", ("#FF0000",)),
            (255, 255, 255): ("mountains", "^", ("#FFFFFF",)),
            (195, 195, 195): ("mountains", "A", ("#C0C0C0",)),
            (127, 127, 127): ("mountains", "A", ("#808080",)),
            (185, 122, 87): ("hills", "~", ("#826644",)),
            (181, 230, 29): ("forest", "T", ("#006400",)),
            (34, 177, 76): ("dark woods", "T", ("#006400",)),
            (255, 201, 14):("plains", ".", ("#568203",)),
            (255, 127, 39): ("plains", ".", ("#FFBD22",)),
            (255, 242, 0): ("fields", "X", ("#FFBF00",)),
            (255, 174, 201): ("desert", "~", ("#F0AC82",)),
            (112, 146, 190): ("river", "~", ("#30FFFF",)),
            (63, 72, 204): ("lake", "-", ("#3088FF",)),
            (0, 162, 232): ("deep seas", "=", ("#3040A0",)),
            (0, 0, 0): ("dungeon", "*", ("#FF00FF",)),
        }  
       
        self.__tile_map = []

        try:
            with Image.open(path) as img:
                pixels = img.load()
                self.width, self.height = img.size
        except FileNotFoundError:
            raise FileNotFoundError(
                "Tilemap: Cannot find file: {}".format(path))

        for j in range(self.height):
            col = []
            for i in range(self.width):
                # sometimes alpha channel is included so test for all values first
                try:
                    r, g, b, _ = pixels[i, j]
                except ValueError:
                    r, g, b = pixels[i, j]
                try:
                    tile_type, tile_char, hexcodes = chars[(r, g, b)]
                except KeyError:
                    raise KeyError("Create Tile Map: '{}' not in keys".format(char))

                hexcode = choice(hexcodes) if len(hexcodes) > 1 else hexcodes[0]
                block_mov = tile_char in self.chars_block_move
                block_lit = tile_char in self.chars_block_light
                # tile_name = cities[(i,j)] if tile_char in ("&", "o", "+", "#") else None
                tile_name = None

                tile = self.WorldTile(
                    char=tile_char,
                    color=hexcode,
                    block_mov=block_mov,
                    block_lit=block_mov, 
                    tile_type=tile_type,
                    tile_name=tile_name)
                    
                col.append(tile)
            self.__tile_map.append(col)

    def save_map_check(self):
        maps_path = "./assets/maps/world/"
        if not os.path.isdir(maps_path):
            print("Picturfy folder does not exist -- Creating 'world' folder")
            os.makedirs(maps_path)

    def save_img(self):
        self.save_map_check()
        file_name = "world.png"
        img = Image.new('RGB', (self.width, self.height))
        draw = ImageDraw.Draw(img)
        for j, row in enumerate(self.tilemap):
            for i, tile in enumerate(row):
                img.load()[i, j] = tuple(toInt(color) for color in splitter(tile.color))
        img.save("./assets/maps/world/" + file_name)
                
    def save_map(self):
        self.save_map_check()
        file_name = "world.txt"
        with open("./assets/maps/world/" + file_name, 'w') as text:
            text.write(str(self))

if __name__ == "__main__":
    w = World(map_img_path="./assets/worldmap.png")
    print(w.__repr__())
    # w.create_tile_map()
    print(w)
    w.save_map()
    w.save_img()
    
    