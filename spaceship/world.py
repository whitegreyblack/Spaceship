import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))+'/../')
from bearlibterminal import terminal as term
from collections import namedtuple
from spaceship.setup import setup, setup_font
from random import choice
from PIL import Image
import shelve

'''Colors
"#ff00ff",

dwarven
"#ff0088",
"#ff0000",

orc
"#ff4400",
"#ff8800",

human
"#ffCC00",
"#ffff00",

elven
"#88ff00",
"#00ff00",

beast
"#00ff88",
"#00ffff",

"#0088ff",
"#0000ff",
'''

class World:
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
    pol_legend = {
        (0, 0, 0): "None",
        (185, 122, 87): "dwarven",
        (34, 177, 76): "elven",
        (237, 28, 36): "beast",
        (181, 230, 29): "elven",
        (255, 201, 14): "human",
        (255, 242, 0): "human",
        (255, 127, 39): "human",
        (255, 174, 201): "orken",
        (136, 0, 21): "dwarven",
        (239, 228, 176): "orken",
    }
    pol_color_key ={
        (0, 0, 0): "black",
        (185, 122, 87): "#550000",
        (34, 177, 76): "#228022",
        (237, 28, 36): "#ff8844",
        (181, 230, 29): "#77ff77",
        (255, 201, 14): "#ffAA00",
        (255, 242, 0): "#ff88ff",
        (255, 127, 39): "#ffff00",
        (255, 174, 201): "#ff2255",
        (136, 0, 21): "#ff0000",
        (239, 228, 176): "#0088ff",
    }
    enterables = ("2302", "#", "&")

    geo_legend = {
        (255, 242, 0): ("field", "2261", ("#FFBF00",)),
        (239, 228, 176): ("shore", "2261", ("#FFFFCC", "#FFFFE0")),
        (34, 177, 76): ("dark forest", "00A5", ("#006400","#568203",)),
        (0, 162, 232): ("deep sea", "2248", ("#3040A0",)),
        (195, 195, 195): ("medium mountains", "2229", ("#C0C0C0","#D3D3D3")),
        (127, 127, 127): ("low mountains", "n", ("#808080", "#A9A9A9",)),
        (255, 255, 255): ("high mountains", "005E", ("#C0C0C0","#D3D3D3")),
        (185, 122, 87): ("hills", "2022", ("#C3B091", "#826644")),
        (237, 28, 36): ("settlement", "2302", ("#00fF00",)),
        (181, 230, 29): ("forest", "0192", ("#228B22", "#74C365")),
        (255, 201, 14):("plains", ".", ("#FFBF00",)),
        (255, 174, 201): ("dunes", "2022", ("#F0AC82",)), #"#C19A6B", "#6C541E"
        (136, 0, 21): ("fortress", "#", ("#FF0000",)),
        (200, 191, 231): ("city", "&", ("#FFFF00",)),
        (112, 146, 190): ("river", "~", ("#30FFFF",)),
        (63, 72, 204): ("lake", "2248", ("#3088FF",)),
        (255, 127, 39): ("hot plains", ".", ("#FFBD22",))
    }
    # def __init__(self, land, territory):
    #     self.geotop(land)
    #     self.geopol(territory)
    tile = namedtuple("Tile", "char color land territory tcol enterable")

    def add_world(self, geo, pol):
        # do some error checking
        with Image.open(geo) as img:
            geopix = img.load()
            gw, gh = img.size
        with Image.open(pol) as img:
            polpix = img.load()
            pw, ph = img.size
        assert (gw, gh) == (pw, ph)

        # width height should be same for both so just use one
        self.w, self.h = pw, ph
        # iterate through maps and pull info from each
        self.data = []
        for j in range(self.h):
            row = []
            for i in range(self.w):
                try:
                    gr, gg, gb, _ = geopix[i, j]
                except ValueError:
                    gr, gg, gb = geopix[i, j]

                try:
                    pr, pg, pb, _ = polpix[i, j]
                except ValueError:
                    pr, pg, pb = polpix[i,j]

                # done with geopix/polpix onto namedtuples                
                land, char, colors = self.geo_legend[(gr, gg, gb)]

                if len(colors) > 1:
                    color = choice(colors)
                else:
                    color = colors[0]
                try:
                    territory = self.pol_legend[(pr, pg, pb)]
                except KeyError:
                    print(((i, j), (pr, pg, pb)))
                    raise

                try:
                    tcolor = self.pol_color_key[(pr, pg, pb)]
                except KeyError:
                    raise

                enterable = char in self.enterables
                row.append(self.tile(char, color, land, territory, tcolor, enterable))
            self.data.append(row)
        self.colorize()

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
        '''Adds colors to seatiles'''

        water = set()
        river = set()
        lakes = set()
        for i in range(self.w):
            for j in range(self.h):
                char, col = self.data[j][i].char, self.data[j][i].color
                if (char, col) == ("2248", "#3040A0") and neighbors(i, j, (-1, 2), (-1, 2), "2248"):
                    water.add((i, j))

                if (char, col) == ("2248","#3088FF") and neighbors(i, j, (-1, 2), (-1, 2), "2248"):
                    lakes.add((i, j))

                if (char, col) == ("~", "#30FFFF"):
                    river.add((i, j, self.river_legend[bitval(i, j)]))

        for i, j in water:
            _, _, l, t, c, e = self.data[j][i]
            self.data[j][i] = self.tile("2248","#3050B0", l, t, c, e)

        for i, j in lakes:
            _, _, l, t, c, e = self.data[j][i]
            self.data[j][i] = self.tile("2248", "#30CCFF", l, t, c, e)

        '''Evaluates river tiles'''
        for i, j, c in river:
            _, _, l, t, tc, e = self.data[j][i]
            self.data[j][i] = self.tile(c, "#30FFFF", l, t, tc, e)

    def draw(self):
        def geotop():
            for j in range(len(self.data)):
                for i in range(len(self.data[j])):
                    if len(self.data[j][i].char) > 1:
                        term.puts(i, j, "[c={}]{}[/c]".format(self.data[j][i].color, chr(int(self.data[j][i].char, 16))))
                    else:
                        term.puts(i, j, "[c={}]{}[/c]".format(self.data[j][i].color, self.data[j][i].char, 16))
            term.refresh() 

        def geopol():
            for j in range(len(self.data)):
                for i in range(len(self.data[j])):
                    char, color, _, terr, tcol, _ = self.data[j][i]
                    if terr != "None":
                        term.puts(i, j, "[c={}]{}[/c]".format(tcol, chr(int("2261", 16))))
                    else:
                        if len(char) > 1:
                            term.puts(i, j, "[c={}]{}[/c]".format(color, chr(int(char, 16))))
                        else:
                            term.puts(i, j, "[c={}]{}[/c]".format(color, char, 16))           
            term.refresh()        

        current = "g"
        while True:
            if current == "g":
                geotop()
            else:
                geopol()
            k = term.read()

            if k == term.TK_CLOSE or k == term.TK_ESCAPE or k == term.TK_Q:
                break
            elif k == term.TK_P and current == "g":
                current = "p"
            elif k == term.TK_G and current == "p":
                current = "g"

if __name__ == "__main__":
    setup()
    setup_font('Ibm_cga', 8, 8)
    term.set("window: size=100x70, cellsize=auto")
    # world = World("./assets/worldmap.png", "./assets/worldmap_territories.png")
    world = World() # empty world
    world.add_world("./assets/worldmap.png", "./assets/worldmap_territories.png")
    world.draw()