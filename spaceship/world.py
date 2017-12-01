import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))+'/../')
from bearlibterminal import terminal as term
from collections import namedtuple
from namedlist import namedlist
from spaceship.screen_functions import center
from spaceship.setup_game import setup, setup_font
from textwrap import wrap
# from objects import Map
from spaceship.tools import bresenhams, scroll
from random import choice
from PIL import Image
from typing import Tuple, Union
import time
import shelve


class World:

    # world dictionaries used in map legends
    enterables = ("2302", "#", "&", "+", "o")
    river_legend = {
        0: "2022",
        1: "2551",
        2: "2550",
        3: "255A",
        4: "2551",
        5: "2551",
        6: "2554",
        7: "2560",
        8: "2550",
        9: "255D",
        10: "2550",
        11: "2569",
        12: "2557",
        13: "2563",
        14: "2566",
        15: "256C",
    }

    # list of city names:
    # islands are not yet entered
    enterable_legend = {
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
    city_descriptions = {
        "Westwatch": "A medium size town that protects the Rane Empire \
            from enemies that approach from the west",
        "Renmar": "The capital city of the Rane Empire and largest city in the west",
        "Tiphmore": "A large merchant town. The new capital for the beast-folk",
    }
    # pol_legend = {
    #     (0, 0, 0): ("None", "black"),
    #     (185, 122, 87): ("dwarven","#ff0000"),
    #     (34, 177, 76): ("elven", "#228022"),
    #     (237, 28, 36): ("beast", "#ff8844"),
    #     (181, 230, 29): ("elven", "#77ff77"),
    #     (255, 201, 14): ("human", "#ffAA00"),
    #     (255, 242, 0): ("human", "#ff88ff"),
    #     (255, 127, 39): ("human", "#ffff00"),
    #     (255, 174, 201): ("orken", "#ff2255"),
    #     (136, 0, 21): ("dwarven", "#550000"),
    #     (239, 228, 176): ("orken", "#dddddd"),
    # }

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

    # king_legend = {
    #     (0, 0, 0): ("None", "black"),
    #     (34, 177, 76): ("Emerald Forest", "#006400"),
    #     (255, 201, 14): ("Zagos", "#FFBF00"),
    #     (237, 28, 36): ("Frostshield", "#880000"),
    #     (136, 0, 21): ("Goldbeard", "#FF0000"),
    #     (181, 230, 29): ("Arundel", "#568203"),
    #     (255, 242, 0): ("Rane", "#FFFF00"),
    #     (255, 127, 39): ("Tempest", "#FF8800"),
    #     (239, 228, 176): ("Endless Dunes", "#FFFF88"),
    #     (255, 174, 201): ("Beast Nation", "#ff88ff"),
    # }

    dungeon_legend = {
        (12, 52): "Pig Beach",
        (20, 57): "Beach Cave",
        (22, 50): "Small Dungeon",
    }

    class Tile:
        def __init__(self, char, color, land, enterable):
            self.char = char
            self.color = color
            self.land = land
            self.enterable = enterable

    # tile = namedlist("Tile", "char color land territory tcol kingdom kcol enterable")

    def __init__(self, width: int, height: int) -> None:
        # level zero is world level -- going "down" increments the level variable
        self.level = 0
        self.map_id = 'world'

        # keep the pointers seperated from world and dungeon/map
        self.world_position = []
        self.map_position = []
        self.name = "Calabaston"
        self._dungeons = set()
        self.map_display_width = width
        self.map_display_height = height
        self.display_key = 0

    def __repr__(self):
        return self.__class__.__name__

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

    def load(self, geo: str, pol: str, king: str) -> None:
        # do some error checking
        # geological map
        with Image.open(geo) as img:
            geopix = img.load()
            gw, gh = img.size

        # # territory map
        # with Image.open(pol) as img:
        #     polpix = img.load()
        #     pw, ph = img.size

        # # kingdom map
        # with Image.open(king) as img:
        #     kingpix = img.load()
        #     kw, kh = img.size

        # # make sure these maps are all the same size since they
        # # are the same map with different properties
        # assert (gw, gh) == (pw, ph)
        # assert (gw, gh) == (kw, kh)

        # width height should be same for both so just use one
        self.width, self.height = gw, gh
        self.map_display_width = min(self.width, self.map_display_width)
        self.map_display_height = min(self.height, self.map_display_height)

        # iterate through maps and pull info from each
        self.data = []
        for j in range(self.height):
            row = []
            for i in range(self.width):

                # seperate the array indexing access by map
                # to decrease confusion on error
                # encapsulate within try/except due to randomness
                # of alpha channel popping up now and then

                # geological map
                try:
                    gr, gg, gb, _ = geopix[i, j]
                except ValueError:
                    gr, gg, gb = geopix[i, j]

                # # territory map
                # try:
                #     pr, pg, pb, _ = polpix[i, j]
                # except ValueError:
                #     pr, pg, pb = polpix[i,j]

                # # kingdom map
                # try:
                #     kr, kg, kb, _ = kingpix[i, j]
                # except ValueError:
                #     kr, kg, kb = kingpix[i, j]

                # done with geo/pol/king -- onto namedtuples                
                # try/except Key-Value used to increase speed of 
                # implementing new properties in map since
                # KeyErrors raises which characters unimplemented

                # deal with geography properties first
                land, char, colors = self.geo_legend[(gr, gg, gb)]
                
                # add to dungeons list
                if char == "*":
                    self._dungeons.add((i,j))

                # differentiate between lists with single or multiple
                # color values to choose from
                if len(colors) > 1:
                    color = choice(colors)
                else:
                    color = colors[0]

                # # then political properties are evaluated
                # try:
                #     territory, tcolor = self.pol_legend[(pr, pg, pb)]
                # except KeyError:
                #     raise KeyError("{}, {}, ({}, {}, {})".format(
                #         i, j, pr, pg, pb
                #     ))

                # # finally kingdom properties
                # try:
                #     kingdom, kcolor = self.king_legend[(kr, kg, kb)]
                # except KeyError:
                #     raise

                enterable = char in self.enterables
                # row.append(self.tile(char, color, land, territory, tcolor, kingdom, kcolor, enterable))
                row.append(self.Tile(char, color, land, enterable))

            self.data.append(row)

        # water and grass tiles are added here 
        self.colorize()
        
        # undecided on whether to add roads or not -- will see in the future if it makes sense to add
        self.build_roads()        
        # empty map data only holds the top level maps -- each map will hold their own sublevel maps
        self.map_data = [[None for _ in range(self.width)] for _ in range(self.height)]
        
    def build_roads(self) -> None:
        '''Creates connections from pointA to pointB on map and writes ROAD characters on the map'''
        def slope(p1, p2):
            x = p2[0] - p1[0]
            y = p2[1] - p1[1]
            if not x:
                return ":"
            if not y:
                return "."
            return ":"
        # -- Cities --
        # "Tiphmore": (42, 62),
        # "Dun Badur": (83, 9),
        # "Aurundel": (41, 20),
        # "Renmar": (16, 46),
        # "Lok Gurrah": (72, 51),   
        # -- Dungeons -- 
        # (12, 52): "Pig Beach",
        # (20, 57): "Beach Cave",
        # (22, 50): "Small Dungeon",
        connections = (
            ((12, 52), (16, 46)),
            ((22, 50), (16, 46)),
            ((26, 57), (20, 57)),
            ((26, 57), (22, 50)),
        )

        for c in connections:
            points = bresenhams(*c)
            char = slope(*c)
            for i, j in points[1:len(points)-1]:
                # _, _, l, t, c, k, kc, e = self.data[j][i]
                # self.data[j][i] = self.tile(char, "#542605", "road", t, c, k, kc, e)    
                
                self.data[j][i] = self.Tile(char, "#542605", "road", self.data[j][i].enterable)    
            
    def colorize(self) -> None:
        '''Colorize modifies lakes and rivers with new characters and colors'''
        def neighbors(i, j, ilim, jlim, v):
            val = 0
            for ii in range(ilim[0], ilim[1]):
                for jj in range(jlim[0], jlim[1]):
                    if (ii, jj) != (0, 0):
                        try:
                            if self.data[j+jj][i+ii].char != v:
                                val += 1
                        except IndexError:
                            pass
            return val > 1

        def grass_neighbors(i, j, v):
            val = 0
            for ii in range(-1, 2):
                for jj in range(-1, 2):
                    if (ii, jj) != (0, 0):
                        try:
                            if self.data[j+jj][i+ii].char == v:
                                val += 1
                        except IndexError:
                            pass
            return val > 0

        def bitval(i, j):
            bit_value=0 
            increment=1
            for ii, jj in ((0,-1), (1,0), (0,1), (-1, 0)):
                    try:
                        char = self.data[j+jj][i+ii].char
                        col = self.data[j+jj][i+ii].color
                    except IndexError:
                        char = ""
                        col = ""
                    if (char, col) in (("~", "#30FFFF"), ("2248","#3040A0"), ("2248","#3088FF")):
                        bit_value += increment
                    increment *= 2
            return bit_value

        water = set()
        river = set()
        lakes = set()
        grass = set()
        plain = set()
        for i in range(self.width):
            for j in range(self.height):
                char, col = self.data[j][i].char, self.data[j][i].color

                # evaluate sea tiles
                # if (char, col) == ("2248", "#3040A0") and neighbors(i, j, (-1, 2), (-1, 2), "2248"):
                #     water.add((i, j))

                # evaluate lake tiles
                # if (char, col) == ("2248","#3088FF") and neighbors(i, j, (-1, 2), (-1, 2), "2248"):
                #     lakes.add((i, j))

                # evaluate river tiles
                # we include return val from river legend since every river tile will be evaluated
                if (char, col) == ("~", "#30FFFF"):
                    river.add((i, j, self.river_legend[bitval(i, j)]))

                # evaluate plain tiles:
                # if (char, col) == (".", "#FFBF00"):
                if (char, col) == (".", "#568203"):

                    plain.add((i, j))
                    if grass_neighbors(i, j, "0192"):
                        # grass.add((i, j))
                        pass
                    elif grass_neighbors(i, j, "="):
                        grass.add((i, j))

        # iterate through sea tiles and replace
        for i, j in water:
            _, _, l, t, c, k, kc, e = self.data[j][i]
            self.data[j][i].char = "="
            # self.data[j][i][0] = "="
            self.data[j][i].color = "#3050B0"

        # iterate through lake tiles and replace
        # for i, j in lakes:
        #     _, _, l, t, c, k, kc, e = self.data[j][i]
        #     self.data[j][i] = self.tile("2248", "#30CCFF", l, t, c, k, kc, e)

        # iterate through river tiles and replace
        for i, j, c in river:
            # _, _, l, t, tc, k, kc, e = self.data[j][i]
            self.data[j][i].char = c
            self.data[j][i].color = "#30FFFF"

        # first pass for grass -- all tiles next to forest or fields
        for i, j in grass:
            # c, _, l, t, tc, k, kc, e = self.data[j][i]
            # self.data[j][i] = self.tile(c, "#228B22", l, t, tc, k, kc, e)
            self.data[j][i].char = "\""
            self.data[j][i].color = "#568203"
            self.data[j][i].land = "grassland"

        # second pass for grass 
        # for i, j in plain:
        #     if self.data[j][i].char == ".":
        #         if grass_neighbors(i, j, "\""):
        #             self.data[j][i].char = "\""
        #             self.data[j][i].color = "#568203" 
        #             self.data[j][i].land = "grassland"

    def enterable(self, i: int, j: int) -> bool:
        return self.data[j][i].enterable

    def access(self, i: int, j: int):
        return self.data[j][i]

    def access_neighbors(self, i: int , j: int):
        # tile = namedtuple("Tile", "char color land territory tcol kingdom kcol enterable")
        neighbors = []
        for jj in range(-1, 2):
            for ii in range(-1, 2):
                if (ii, jj) != (0, 0):
                    try:
                        neighbors.append(self.data[j+jj][i+ii])
                    except IndexError:
                        neighbors.append(self.data[j][i])

        # make sure we get all neighbors
        assert len(neighbors) == 8
        return neighbors

    def legend(self) -> Tuple[str, str, str, int]:
        i = 0
        for d, ch, colors in self.geo_legend.values():
            ch = ch if len(ch) == 1 else chr(int(ch, 16))
            for col in colors:
                yield ch, col, d, i
                i += 1

    def dungeon(self, x: int, y: int):
        return (x, y) in self._dungeons

    def mapAt(self, x: int, y: int):
        return self.map_data[y][x] != None

    def get_location(self, x: int, y: int):
        return self.map_data[y][x]

    def get_landtype(self, x: int, y: int) -> str:
        return self.data[y][x].land

    def is_wilderness(self, x: int, y: int) -> bool:
        for landtype in ("dungeon", "city(human)", "city(elven)", "fortress"):
            if landtype == self.get_landtype(x, y):
                return False
        return True

    def add_location(self, location, x: int, y: int) -> None:
        '''Must've been located in enterables legend'''
        self.map_data[y][x] = location

    def walkable(self, i: int, j: int) -> bool:
        if 0 <= i < self.width and 0 <= j < self.height:
            for landtype in ("sea", "mnts", "lake"):
                if landtype in self.data[j][i].land:
                    return False
            return True
        return False

    def draw(self, player_x: int, player_y: int) -> Tuple[int, int, str, str]:
        
        # map size checks for when the map dimensions are not 80 x 50
        shorten_x = self.map_display_width >= 66
        shorten_y = self.map_display_height >= 44

        # get camera location for x coordinate
        cam_x = scroll(
            player_x, 
            self.map_display_width + (-15 if shorten_x else 0), 
            self.width)
        ext_x = cam_x + self.map_display_width + (-15 if shorten_x else 0)

        # get camera location for y coordinate
        cam_y = scroll(
            player_y, 
            self.map_display_height + (-2 if shorten_y else -2), 
            self.height)
        ext_y = cam_y + self.map_display_height + (-2 if shorten_y else -2)

        for j in range(cam_y, ext_y):
            for i in range(cam_x, ext_x):
                if (player_x, player_y) == (i, j):
                    color = "white"
                    char = "@"
                else:
                    try:
                        # char, color, _, terr, tcol, king, kcol, _ = self.data[j][i]
                        tile = self.data[j][i]
                    except IndexError:
                        raise IndexError("{}, {}".format(i, j))
                    
                    char = tile.char
                    
                    if len(char) > 1:
                        try:
                            char = chr(int(char, 16))
                        except ValueError:
                            raise ValueError(char)

                    color = tile.color

            
                # if self.display_key == 0:
                #     if len(char) > 1:
                #         try:
                #             char = chr(int(char, 16))
                #         except ValueError:
                #             raise ValueError(char)

                # elif self.display_key == 1:
                #     color = tcol
                #     if terr != "None":
                #         char = chr(int("2261", 16))
                #     else:
                #         if len(char) > 1:
                #             char = chr(int(char, 16))
                
                # else:
                #     color = kcol
                #     if king != "None:":
                #         char = chr(int("2261", 16))
                #     elif len(char) > 1:
                #         char = chr(int(char, 16))
                
                yield (i-cam_x, j-cam_y, color, char)

    
if __name__ == "__main__":
    # FH, FW, GH, GW = 8, 8, 25, 40
    setup()
    FH, FW, GH, GW = 16, 16, 24, 40
    setup_font('Ibm_cga', FW, FH)
    term.set("window: size={}x{}, cellsize=auto".format(GW, GH))

    world = World() # adding character which will be passed down everywhere
    world.load(
        "./assets/worldmap.png", 
        "./assets/worldmap_territories.png",
        "./assets/worldmap_kingdoms.png")
    world.testdraw()
