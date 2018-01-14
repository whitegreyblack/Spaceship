import os
import sys
from typing import Tuple, Union
from PIL import Image, ImageDraw
from collections import namedtuple
from random import shuffle, choice, randint
from .charmap import WildernessCharmap as wcm
from .charmap import DungeonCharmap as dcm
from .charmap import WorldCharmap as ccm
from .utils import splitter, blender
from ..tools import toInt, scroll
from .map import Map

'''
Calabaston : Roguelike
    Game: {
        Planet: {
            Name: Unknown,
                Ecology: {
                    Hills,
                    Plains,
                    Forests,
                    Dark Woods,
                    Grasslands,
                    Mountains,
                    Rivers,
                    Oceans,
                    Seas,
                    },
                Races: {
                    Orcs,
                    Elves,
                    Beasts,
                    Humans,
                    Dwarves,
                    Demons, # -- maybe
                    Monsters # -- all of them
                }
            Continents: {
            Calabaston: {
                Countries: {
                Empire of Rane: {
                    Capital: Renmar,
                    Cities: {
                    Shadowbarrow,
                    Westwatch,
                    Lakepost,     
                    Northshore,         
                    }
                },
                Highlands: {
                    Cities: {
                    Dun Kaldergan,
                    Dun Mogan,
                    Dun Badur,
                    Dun Baras,
                    Dun Caden,
                    Dun Molbur,
                    Dun Vargar,
                    }
                },
                Lowlands: {
                    Capital: Gom Bashur,
                    Cities: {
                    Lok Zargoth,
                    Lok Gurrah,
                    Lok Midgoth,
                    Lok Toragoth,
                    Gorrathah,
                    }
                }
                Aurendelim: {
                    Capital: Aurendel,
                    Cities: {
                    Falaeth,
                    Aerathalar,
                    Galaloth,
                    Runagathor,
                    Lantathor,
                    Elenos,
                    Elenloth,
                    }
                },
                Free Cities: {
                    Fragos,
                    Yarrin,
                    Tiphmore,
                    Houndsbeach,
                    Dawnvalley,
                    Eastshore,
                    Whitewater,
                }
            },
            Dungeons: {
            Pigs Beach,
            Small Dungeon,
            Beach Cave,
            }
        },
        Merma: Unknown,
        Decadon: Unknown,
        Rygor: Unknown,
    }
  }
}
'''

class World(Map):
    chars = {
        "&": (["&"], "#FF8844"),
    }
    chars_block_move = ["=", "-", 'A', '^']
    chars_block_light = ["T", "^", "~", "A", "^"]

    enterable_legend = {
        (5, 28): "Northshore",
        (51, 42): "Aerathalar",
        (12, 14): "Armagos",
        (41, 20): "Aurundel",
        (53, 51): "Dawnvalley",
        (83, 9): "Dun Badur",
        (63, 7): "Dun Baras",
        (55, 14): "Dun Caden",
        (82, 19): "Dun Kaldergen",
        (88, 28): "Dun Mogan",
        (48, 14): "Dun Molbur",
        (33, 7): "Dun Vargar",
        (65, 36): "Eastshore",
        (91, 40): "Elenloth",
        (78, 34): "Elenos",
        (31, 18): "Falaeth",
        (6, 10): "Fragos",
        (25, 32): "Galaloth",
        (91, 55): "Gom Bashur",
        (96, 48): "Gorrathah",
        (12, 14): "Houndsbeach",
        (69, 22): "Lantathor",
        (44, 35): "Lakepost",
        (72, 51): "Lok Gurrah",
        (69, 62): "Lok Midgoth",
        (82, 60): "Lok Toragath",
        (82, 45): "Lok Zargoth",
        (16, 46): "Renmar",
        (58, 26): "Runagathor",
        (26, 57): "Shadowbarrow",
        (42, 62): "Tiphmore",
        (7, 43): "Westwatch",
        (67, 42): "Whitewater",
        (21, 18): "Yarrin",
    }

    capitals = {

    }

    geo_legend = {
        (200, 191, 231): ("city(elven)", "&", ("#FF8844",)),
        (153, 217, 234): ("fort(dwarf)", "#", ("#FF00FF",)),
        (163, 73, 164): ("city(elven)", "&", ("#FFFF00",)),
        # (237, 28, 36): ("city(human)", "2302", ("#00fF00",)),
        (237, 28, 36): ("city(human)", "+", ("#00fF00",)),
        (136, 0, 21): ("fort(orcen)", "o", ("#FF0000",)),
        # (239, 228, 176): ("shore", "2261", ("#FFFFCC", "#FFFFE0")),
        (255, 255, 255): ("mnts(high)", "005E", ("#FFFFFF",)),
        # (195, 195, 195): ("mnts(med)", "2229", ("#C0C0C0",)),
        (195, 195, 195): ("mnts(med)", "n", ("#C0C0C0",)),

        # (127, 127, 127): ("mnts(low)", "n", ("#808080", "#A9A9A9",)),
        (127, 127, 127): ("mnts(low)", "n", ("#808080",)),

        # (185, 122, 87): ("hills", "2022", ("#C3B091", "#826644")),
        (185, 122, 87): ("hills", "2022", ("#826644",)),
        # (181, 230, 29): ("forest", "0192", ("#228B22", "#74C365")),
        # (181, 230, 29): ("forest", "0192", ("#568203",)),
        (181, 230, 29): ("forest", "0192", ("#006400",)),

        # (34, 177, 76): ("dark woods", "00A5", ("#006400","#568203",)),
        (34, 177, 76): ("dark woods", "00A5", ("#006400",)),
        # (255, 201, 14):("plains", ".", ("#FFBF00",)),
        (255, 201, 14):("plains", ".", ("#568203",)),

        (255, 127, 39): ("plains", ".", ("#FFBD22",)),
        # (255, 242, 0): ("fields", "2261", ("#FFBF00",)),
        (255, 242, 0): ("fields", "=", ("#FFBF00",)),
        (255, 174, 201): ("desert", "~", ("#F0AC82",)),
        (112, 146, 190): ("river", "~", ("#30FFFF",)),
        (63, 72, 204): ("lake", "2248", ("#3088FF",)),
        (0, 162, 232): ("deep seas", "2248", ("#3040A0",)),
        (0, 0, 0): ("dungeon", "*", ("#FF00FF",)),
    }
    dungeon_legend = {
        (12, 52): "Pig Beach",
        (20, 57): "Beach Cave",
        (22, 50): "Small Dungeon",
    }
    # class WorldTile(Map.Tile):
    class WorldTile:
        def __init__(self, char, color, block_mov, block_lit, tile_type, tile_name=None):
            '''Inherits from Map.Tile to create a tile specific for a world map'''
            # super().__init__(char, color, block_mov, block_lit)
            self.char = char
            self.color = color
            self.block_mov = block_mov
            self.block_lit = block_lit
            self.tile_type = tile_type
            self.light = 0
            if tile_name:
                self.name = tile_name

        def __repr__(self):
            return self.char

        def __str__(self):
            return "{}, {}, {}, {}, {}".format(
                self.char,
                self.color,
                self.block_mov,
                self.block_lit,
                self.light)

    def __init__(self, map_name, map_link):
        self.map_name = map_name
        self.tilemap = map_link
        self.locations = {}
        super().__init__(self.width, self.height, self.__class__.__name__)

    def __repr__(self):
      return "{}: ({}, {})".format(
        self.__class__.__name__,
        self.width, self.height)

    def __str__(self):
        return "\n".join("".join(tile.char for tile in row) for row in self.tilemap)

    @staticmethod
    def capitals(capital: str) -> str:
        city = {
            "Tiphmore": (42, 62),
            "Dun Badur": (83, 9),
            "Aurundel": (41, 20),
            "Renmar": (16, 46),
            "Lok Gurrah": (72, 51),            
        }

        return city[capital]

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
                block_lit = tile_char not in self.chars_block_light
                # tile_name = cities[(i,j)] if tile_char in ("&", "o", "+", "#") else None
                tile_name = None

                tile = self.WorldTile(
                    char=tile_char,
                    color=hexcode,
                    block_mov=block_mov,
                    block_lit=block_lit, 
                    tile_type=tile_type,
                    tile_name=tile_name)
                # print(tile)
                col.append(tile)
            self.__tile_map.append(col)

    def save_map_check(self):
        maps_path = "./spaceship/assets/maps/world/"
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
        img.save("./spaceship/assets/maps/world/" + file_name)
                
    def save_map(self):
        self.save_map_check()
        file_name = "world.txt"
        with open("./spaceship/assets/maps/world/" + file_name, 'w') as text:
            text.write(str(self))

    def legend(self) -> Tuple[str, str, str, int]:
        i = 0
        for d, ch, colors in self.geo_legend.values():
            ch = ch if len(ch) == 1 else chr(int(ch, 16))
            for col in colors:
                yield ch, col, d, i
                i += 1

    def location_exists(self, x, y):
        return (x, y) in self.locations.keys()

    def location_is(self, x, y, v):
        # print("MAPTYPE:", self.locations[(x, y)].map_type)
        return self.locations[(x, y)].map_type == v

    def location_create(self, x, y, location):
        self.locations[(x, y)] = location

    def location(self, x, y):
        return self.locations[(x, y)]
    # @property
    # def location(self, x, y):
    #     '''Returns map if exists else None'''
    #     try:
    #         return self.locations[(x, y)]
    #     except KeyError:
    #         return None

    # @location.setter
    # def location(self, x, y, l):
    #     '''Sets location at (x, y)'''
    #     self.locations[(x, y)] = l

    def landtype(self, x, y):
        return self.square(x, y).tile_type

    def output(self, player_x, player_y):
        shorten_x = self.map_display_width > 66
        shorten_y = self.map_display_height > 44

        # get camera location for x coordinate
        cam_x = scroll(
            player_x, 
            self.map_display_width + (-14 if shorten_x else 0), 
            self.width)
        ext_x = cam_x + self.map_display_width + (-14 if shorten_x else 0)

        # get camera location for y coordinate
        cam_y = scroll(
            player_y, 
            self.map_display_height + (-6 if shorten_y else 0), 
            self.height)
        ext_y = cam_y + self.map_display_height + (-6 if shorten_y else 0)
        
        for y in range(cam_y, ext_y):
            for x in range(cam_x, ext_x):
                light_level = self.check_light_level(x, y)
                if x == player_x and y == player_y:
                    ch, col = "@", "white"

                elif light_level == 2:
                    square = self.square(x, y)
                    ch, col = square.char, square.color

                elif light_level == 1:
                    square = self.square(x, y)
                    ch, col = square.char, "darkest grey"

                else:
                    continue
                # else:
                #     try:
                #         # char, color, _, terr, tcol, king, kcol, _ = self.data[j][i]
                #         tile = self.square(x, y)
                #     except IndexError:
                #         raise IndexError("{}, {}".format(x, y))
                    
                #     ch = tile.char
                    
                #     if len(ch) > 1:
                #         try:
                #             ch = toInt(ch)
                #         except ValueError:
                #             raise ValueError(ch)

                #     col = tile.color

                # print(ch, col)
                yield (x - cam_x, y - cam_y, col, ch)
        self.lit_reset()

if __name__ == "__main__":
    w = World(
        map_name="Calabaston",
        map_link="./spaceship/assets/worldmap.png")
    print(w.__repr__())
    # w.create_tile_map()
    print(w)
    w.save_map()
    w.save_img()