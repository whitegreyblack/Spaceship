import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))+'/../')
from bearlibterminal import terminal as term
from spaceship.maps import stringify, picturfy
from spaceship.setup import setup, setup_font

class World:
    def __init__(self, string):
        self.data = stringify(string).split('\n')
        self.height = len(self.data)
        self.width = len(self.data[0])

    def draw(self):
        for j in range(len(self.data)):
            for i in range(len(self.data[j])):
                term.puts(i, j, self.data[j][i])
        term.refresh()
        term.read()

if __name__ == "__main__":
    setup()
    setup_font('Ibm_cga', 8, 8)
    term.set("window: size=80x50")
    world = World("./assets/worldmap.png")
    world.draw()