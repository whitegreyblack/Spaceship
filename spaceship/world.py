import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))+'/../')
from bearlibterminal import terminal as term
from spaceship.setup import setup, setup_font
from random import choice
from PIL import Image

class World:
    legend = {
        (255, 242, 0): ("00A5", ("#FFBF00", "#F0DC82")),
        # (239, 228, 176): ("2219", ("#FFFFCC", "#FFFFE0", "#EDC9AF")),
        (239, 228, 176): ("2261", ("#FFFFCC", "#FFFFE0")),
        (0, 0, 0): ("#", ""),
        (34, 177, 76): ("0192", ("#006400","#568203",)),
        (0, 162, 232): ("2248", ("#0040A0",)),
        (195, 195, 195): ("~", ("#808080", "#A9A9A9", "#C0C0C0","#D3D3D3")),
        (255, 255, 255): ("005E", ("#C0C0C0","#D3D3D3")),
        (185, 122, 87): ("~", ("#C3B091", "#826644")),
        (237, 28, 36): ("2302", ("#00E0E0",)),
        (181, 230, 29): ("0192", ("#228B22", "#74C365")),
        (255, 201, 14):(".", ("#87A96B","#4B6F44")),
        (255, 174, 201): ("~", ("#EDC9AF","#C19A6B", "#6C541E")),
        (136, 0, 21): ("#", ("#00E0E0",)),
        (200, 191, 231): ("&", ("#00E0E0",)),
    }
    def __init__(self, string):
        self.stringify(string)

    def stringify(self, string):
        '''Only called once for world load'''
        with Image.open(string) as img:
            pixels = img.load()
            self.w, self.h = img.size
            print(self.w, self.h)
        lines = []
        for j in range(self.h):
            line = []
            for i in range(self.w):
                # sometimes alpha channel is included so test for all values first
                try:
                    r, g, b, _ = pixels[i, j]
                except ValueError:
                    r, g, b = pixels[i, j]
                try:
                    try:
                        char, colors = self.legend[(r, g, b)]
                        # if char == "2248":
                        #     print(colors)
                    except ValueError:
                        char = self.legend[(r, g, b)]
                    if not colors:
                        colors = ("#ffffff")
                    if len(colors) > 1:
                        color = choice(colors)
                    else:
                        color = colors[0]
                    line.append((char, color))
                except KeyError:
                    print((r, g, b))
                    line.append(" ")
            lines.append(line)

        self.data = lines
        self.colorize()

    def colorize(self):
        def neighbors(i, j, ilim, jlim, v):
            val = 0
            for ii in range(ilim[0], ilim[1]):
                for jj in range(jlim[0], jlim[1]):
                    if (ii, jj) != (0, 0):
                        try:
                            if self.data[j+jj][i+ii][0] != v:
                                val += 1
                        except IndexError:
                            pass
            return val > 1

        '''Adds colors to water'''
        water = set()
        for i in range(self.w):
            for j in range(self.h):
                if self.data[j][i][0] == "2248" and neighbors(i, j, (-1, 2), (-1, 2), "2248"):
                    water.add((i, j))
        for i, j in water:
            self.data[j][i] = ("2248", "#0060D0")

    def draw(self):
        while True:
            for j in range(len(self.data)):
                for i in range(len(self.data[j])):
                    if len(self.data[j][i][0]) > 1:
                        term.puts(i, j, "[c={}]{}[/c]".format(self.data[j][i][1], chr(int(self.data[j][i][0], 16))))
                    else:
                        term.puts(i, j, "[c={}]{}[/c]".format(self.data[j][i][1], self.data[j][i][0], 16))
            term.refresh()
            k = term.read()
            if k == term.TK_CLOSE or k == term.TK_ESCAPE or k == term.TK_Q:
                break

if __name__ == "__main__":
    setup()
    setup_font('Ibm_cga', 8, 8)
    term.set("window: size=100x70, cellsize=auto")
    world = World("./assets/worldmap.png")
    world.draw()