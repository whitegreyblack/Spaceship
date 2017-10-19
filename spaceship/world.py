import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))+'/../')
from bearlibterminal import terminal as term
from collections import namedtuple
from namedlist import namedlist
from spaceship.screen_functions import center
from spaceship.setup import setup, setup_font
from spaceship.maps import stringify
from textwrap import wrap
# from objects import Map
from random import choice
from PIL import Image
import time
import shelve


class World:
    # world dictionaries used in map legends
    enterables = ("2302", "#", "&")
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
        (93, 25): "Dun Mogan",
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

    pol_legend = {
        (0, 0, 0): ("None", "black"),
        (185, 122, 87): ("dwarven","#ff0000"),
        (34, 177, 76): ("elven", "#228022"),
        (237, 28, 36): ("beast", "#ff8844"),
        (181, 230, 29): ("elven", "#77ff77"),
        (255, 201, 14): ("human", "#ffAA00"),
        (255, 242, 0): ("human", "#ff88ff"),
        (255, 127, 39): ("human", "#ffff00"),
        (255, 174, 201): ("orken", "#ff2255"),
        (136, 0, 21): ("dwarven", "#550000"),
        (239, 228, 176): ("orken", "#dddddd"),
    }

    geo_legend = {
        (200, 191, 231): ("city(elven)", "&", ("#FFFF00",)),
        (237, 28, 36): ("city(human)", "2302", ("#00fF00",)),
        (136, 0, 21): ("fort(dw/or)", "#", ("#FF0000",)),
        # (239, 228, 176): ("shore", "2261", ("#FFFFCC", "#FFFFE0")),
        (255, 255, 255): ("mnts(high)", "005E", ("#D3D3D3",)),
        (195, 195, 195): ("mnts(med)", "2229", ("#C0C0C0",)),
        (127, 127, 127): ("mnts(low)", "n", ("#808080", "#A9A9A9",)),
        (185, 122, 87): ("hills", "2022", ("#C3B091", "#826644")),
        (181, 230, 29): ("forest", "0192", ("#228B22", "#74C365")),
        (34, 177, 76): ("dark woods", "00A5", ("#006400","#568203",)),
        (255, 201, 14):("plains", ".", ("#FFBF00",)),
        (255, 127, 39): ("plains", ".", ("#FFBD22",)),
        (255, 242, 0): ("fields", "2261", ("#FFBF00",)),
        (255, 174, 201): ("deserts", "~", ("#F0AC82",)),
        (112, 146, 190): ("rivers", "~", ("#30FFFF",)),
        (63, 72, 204): ("lakes", "2248", ("#3088FF",)),
        (0, 162, 232): ("deep seas", "2248", ("#3040A0",)),
        (0, 0, 0): ("dungeons", "*", ("#8800FF",)),
    }

    king_legend = {
        (0, 0, 0): ("None", "black"),
        (34, 177, 76): ("Emerald Forest", "#006400"),
        (255, 201, 14): ("Zagos", "#FFBF00"),
        (237, 28, 36): ("Frostshield", "#880000"),
        (136, 0, 21): ("Goldbeard", "#FF0000"),
        (181, 230, 29): ("Arundel", "#568203"),
        (255, 242, 0): ("Rane", "#FFFF00"),
        (255, 127, 39): ("Tempest", "#FF8800"),
        (239, 228, 176): ("Endless Dunes", "#FFFF88"),
        (255, 174, 201): ("Beast Nation", "#ff88ff"),
    }

    tile = namedtuple("Tile", "char color land territory tcol kingdom kcol enterable")

    def __init__(self):
        self.pointer = (0, 0)
        # empty map data only holds the top level maps -- each map will hold their own sublevel maps
        self.map_data = {} 
        # level zero is world level -- going "down" increments the level variable
        self.level = 0

        # keep the pointers seperated from world and dungeon/map
        self.world_position = []
        self.map_position = []
        self.name = "Calabaston"

    @staticmethod
    def capitals(capital):
        city = {
            "Tiphmore": (42, 62),
            "Dun Badur": (83, 9),
            "Aurundel": (41, 20),
            "Renmar": (16, 46),
            "Lok Gurrah": (72, 51),            
        }

        return city[capital]

    def load(self, geo, pol, king):
        # do some error checking
        with Image.open(geo) as img:
            geopix = img.load()
            gw, gh = img.size
        with Image.open(pol) as img:
            polpix = img.load()
            pw, ph = img.size
        with Image.open(king) as img:
            kingpix = img.load()
            kw, kh = img.size
        assert (gw, gh) == (pw, ph)
        assert (gw, gh) == (kw, kh)

        # width height should be same for both so just use one
        self.w, self.h = pw, ph
        # iterate through maps and pull info from each
        self.data = []
        for j in range(self.h):
            row = []
            for i in range(self.w):

                # seperate the array indexing access by map
                # to decrease confusion on error
                # encapsulate within try/except due to randomness
                # of alpha channel popping up now and then
                try:
                    gr, gg, gb, _ = geopix[i, j]
                except ValueError:
                    gr, gg, gb = geopix[i, j]

                try:
                    pr, pg, pb, _ = polpix[i, j]
                except ValueError:
                    pr, pg, pb = polpix[i,j]

                try:
                    kr, kg, kb, _ = kingpix[i, j]
                except ValueError:
                    kr, kg, kb = kingpix[i, j]

                # done with geo/pol/king -- onto namedtuples                
                # try/except KV used to increase speed of 
                # implementing new properties in map

                # deal with geography properties first
                land, char, colors = self.geo_legend[(gr, gg, gb)]

                if len(colors) > 1:
                    color = choice(colors)
                else:
                    color = colors[0]

                # then political properties
                try:
                    territory, tcolor = self.pol_legend[(pr, pg, pb)]
                except KeyError:
                    print(((i, j), (pr, pg, pb)))
                    raise

                # finally kingdom properties
                try:
                    kingdom, kcolor = self.king_legend[(kr, kg, kb)]
                except KeyError:
                    raise

                enterable = char in self.enterables
                row.append(self.tile(char, color, land, territory, tcolor, kingdom, kcolor, enterable))
            self.data.append(row)
        self.colorize()
        return self

    def colorize(self):
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
        for i in range(self.w):
            for j in range(self.h):
                char, col = self.data[j][i].char, self.data[j][i].color

                # evaluate sea tiles
                # if (char, col) == ("2248", "#3040A0") and neighbors(i, j, (-1, 2), (-1, 2), "2248"):
                #     water.add((i, j))

                # evaluate lake tiles
                # if (char, col) == ("2248","#3088FF") and neighbors(i, j, (-1, 2), (-1, 2), "2248"):
                #     lakes.add((i, j))

                # evaluate river tiles
                if (char, col) == ("~", "#30FFFF"):
                    river.add((i, j, self.river_legend[bitval(i, j)]))

        # iterate through sea tiles and replace
        for i, j in water:
            _, _, l, t, c, k, kc, e = self.data[j][i]
            self.data[j][i] = self.tile("=","#3050B0", "sea", t, c, k, kc, e)


        # iterate through lake tiles and replace
        # for i, j in lakes:
        #     _, _, l, t, c, k, kc, e = self.data[j][i]
        #     self.data[j][i] = self.tile("2248", "#30CCFF", l, t, c, k, kc, e)

        # iterate through river tiles and replace
        for i, j, c in river:
            _, _, l, t, tc, k, kc, e = self.data[j][i]
            self.data[j][i] = self.tile(c, "#30FFFF", l, t, tc, k, kc, e)

    def enterable(self, i, j):
        return self.data[j][i].enterable

    def accessTile(self, i, j):
        return self.data[j][i]

    def maplegend(self):
        i = 0
        for d, ch, colors in self.geo_legend.values():
            ch = ch if len(ch) == 1 else chr(int(ch, 16))
            for col in colors:
                yield ch, col, d, i
                i += 1

    def add_city(self, x, y, gw, gh):
        '''Must've been located in enterables legend'''
        # try:
        #     string = "./assets/maps/"+self.enterable_legend[(x, y)].lower().replace(' ','_')+".png"
        #     self.map_data[(x, y)] = Map(stringify(string), gw, gh)
        #     print("loaded {}".format(string))
        # except FileNotFoundError:
        #     pass
        pass

    def add_dungeon(self, x, y):
        '''Must've been located in dungeontile?'''
        pass

    def walkable(self, i, j):
        if 0 <= i < self.w-1 and 0 <= j < self.h-1:
            for landtype in ("sea", "mnts", "lake"):
                if landtype in self.data[j][i].land:
                    return False
            return True
        return False

    def draw(self, key, x, y, vx, vy):
        for j in range(*vy):
            for i in range(*vx):
                try:
                    char, color, _, terr, tcol, king, kcol, _ = self.data[j][i]
                except IndexError:
                    print(i, j)
                    raise

                if (x, y) == (i, j):
                    color = "white"
                    char = "@"

                if key == 0:
                    if len(char) > 1:
                        char = chr(int(char, 16))

                elif key == 1:
                    color = tcol
                    if terr != "None":
                        char = chr(int("2261", 16))
                    else:
                        if len(char) > 1:
                            char = chr(int(char, 16))
                
                else:
                    color = kcol
                    if king != "None:":
                        char = chr(int("2261", 16))
                    elif len(char) > 1:
                        char = chr(int(char, 16))
                
                yield (i-vx[0], j-vy[0], color, char)
    """
    def testdraw(self):
        '''probably should only be called on main script'''
        def scroll(position, screen, worldmap):
            '''
            @position: current position of player 1D axis
            
            @screen  : size of the screen
            
            @worldmap: size of the map           
            '''
            halfscreen = screen//2
            # less than half the screen - nothing
            if position < halfscreen:
                return 0
            elif position >= worldmap - halfscreen:
                return worldmap - screen
            else:
                return position - halfscreen

        def geotop():
            for j in range(cy, cy+GH-1):
                for i in range(cx, cx+GW):
                    if len(self.data[j][i].char) > 1:
                        term.puts(i-cx, j-cy+1, "[c={}]{}[/c]".format(self.data[j][i].color, chr(int(self.data[j][i].char, 16))))
                    else:
                        term.puts(i-cx, j-cy+1, "[c={}]{}[/c]".format(self.data[j][i].color, self.data[j][i].char))
            term.bkcolor('white')
            term.puts(0, 0, "#"*GW)
            term.puts(center("Geography of Calabaston  ", GW), 0,
                "[c=black]Geography of Calabaston[/c]")
            term.bkcolor('black')

        def geopol():
            for j in range(cy, cy+GH-1):
                for i in range(cx, cx+GW):
                    char, color, _, terr, tcol, _, _, _ = self.data[j][i]
                    if terr != "None":
                        term.puts(i-cx, j-cy+1, "[c={}]{}[/c]".format(tcol, chr(int("2261", 16))))
                    else:
                        if len(char) > 1:
                            term.puts(i-cx, j-cy+1, "[c={}]{}[/c]".format(color, chr(int(char, 16))))
                        else:
                            term.puts(i-cx, j-cy+1, "[c={}]{}[/c]".format(color, char))     
            term.bkcolor('white')
            term.puts(0, 0, "#"*GW)
            term.puts(center("Territories of Calabaston  ", GW), 0,
                "[c=black]Territories of Calabaston[/c]")
            term.bkcolor('black')      

        def geoking():
            for j in range(cy, cy+GH-1):
                for i in range(cx, cx+GW):
                    char, color, _, _, _, k, kc, _ = self.data[j][i]
                    if k != "None":
                        term.puts(i-cx, j-cy+1, "[c={}]{}[/c]".format(kc, chr(int("2261", 16))))
                    else:
                        if len(char) > 1:
                            term.puts(i-cx, j-cy+1, "[c={}]{}[/c]".format(color, chr(int(char, 16))))
                        else:
                            term.puts(i-cx, j-cy+1, "[c={}]{}[/c]".format(color, char, 16))    
            term.bkcolor('white')
            term.puts(0, 0, "#"*GW)
            term.puts(center("Kingdoms of Calabaston  ", GW), 0,
                "[c=black]Kingdoms of Calabaston[/c]")
            term.bkcolor('black')     

        global GH, GW, FH, FW
        current = "g"
        lastposition = None
        while True:
            x, y = self.pointer
            cx = scroll(self.pointer[0], GW, self.w)
            cy = scroll(self.pointer[1], GH-1, self.h)

            term.clear()
            if self.level <= 0:
                print(self.level)
                if current == "g":
                    geotop()
                elif current == "p":
                    geopol()
                else:
                    geoking()
                term.puts(x-cx, y-cy+1, '[c=white]@[/c]')
                if self.enterable(x, y):
                    term.bkcolor('white')
                    term.puts(0, GH-1, "#"*GW)    
                    try:                
                        term.puts(center("  "+self.enterable_legend[(x, y)], GW), GH-1, 
                            "[c=black]"+self.enterable_legend[(x, y)]+"[/c]")
                    except KeyError:
                        term.puts(center("  "+"Some town : to be named", GW), GH-1, 
                            "[c=black]Some town : to be named[/c]")
                    term.bkcolor("black")

            else:
                if (x, y) not in self.map_data.keys():
                    term.puts(center("nodata  ", GW), GH//2, "NO DATA")    
                else:
                    # self.level += 1
                    print(self.level)
                    term.puts(center("nodata  ", GW), GH//2, "LOAD MAP")    
                    dungeon = self.map_data[(x, y)]
                    xx, yy = dungeon.width//2, dungeon.height//2
                    dungeon.fov_calc([(xx, yy, 5),])
                    for i, j, lit, ch, bkgd in list(dungeon.output(xx, yy, [])):
                        term.puts(i, j, "[color={}]".format(lit)+ch+"[/color]")

            term.refresh()

            k = term.read()
            print(k)
            while k in (term.TK_SHIFT, term.TK_ALT, term.TK_CONTROL):
                k = term.read()

            # exit logic
            if k == term.TK_CLOSE or k == term.TK_ESCAPE or k == term.TK_Q:
                break

            # map functions
            elif k == term.TK_P and current != "p":
                current = "p"
            elif k == term.TK_G and current != "g":
                current = "g"
            elif k == term.TK_K and current != "k":
                current = "k"

            # level switching
            elif k == term.TK_PERIOD:
                if term.state(term.TK_SHIFT) and self.enterable(x, y):
                    print('entering')                
                    self.level += 1
                    if (x, y) not in self.map_data.keys():
                        print('no data')
                        # if it is a city
                        if (x, y) in self.enterable_legend.keys():
                            self.add_city(x, y, GW, GH)

            elif k == term.TK_COMMA:
                if term.state(term.TK_SHIFT):
                    print('exitting')                
                    self.level -= 1


            # terminal zooming
            elif k == term.TK_Z:
                change = False
                if term.TK_Z and term.state(term.TK_SHIFT):
                    if (GH, GW) != (24, 40):
                        FH, FW, GH, GW = 16, 16, 24, 40
                        change = True
                        self.level += 1
                else:   
                    if (GH, GW) != (48, 80):
                        FH, FW, GH, GW = 8, 8, 48, 80
                        change = True
                        self.level -= 1
                if change:
                    setup_font('Ibm_cga', FW, FH)
                    term.set("window: size={}x{}, cellsize=auto".format(GW, GH))

            # movement key handling
            elif k == term.TK_UP and self.level == 0:
                print(self.level, 'walking')
                if self.walkable(x, y-1):
                    y -= 1
            elif k == term.TK_DOWN and self.level == 0:
                if self.walkable(x, y+1):
                    y += 1
            elif k == term.TK_LEFT and self.level == 0:
                if self.walkable(x-1, y):
                    x -= 1
            elif k == term.TK_RIGHT and self.level == 0:
                if self.walkable(x+1, y):
                    x += 1
            self.pointer[0] = max(min(x, self.w-1), 0)
            self.pointer[1] = max(min(y, self.h), 1)
            self.level = max(min(self.level, 1), -1)
    """
if __name__ == "__main__":
    # FH, FW, GH, GW = 8, 8, 25, 40
    setup()
    FH, FW, GH, GW = 16, 16, 24, 40
    setup_font('Ibm_cga', FW, FH)
    term.set("window: size={}x{}, cellsize=auto".format(GW, GH))

    world = World(None) # adding character which will be passed down everywhere
    world.load(
        "./assets/worldmap.png", 
        "./assets/worldmap_territories.png",
        "./assets/worldmap_kingdoms.png")
    world.testdraw()