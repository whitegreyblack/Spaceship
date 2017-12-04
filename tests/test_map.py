import os
import sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))+'/../')
from bearlibterminal import terminal as t
from spaceship.maps.city import City
from spaceship.maps.cave import Cave
from spaceship.units.monsters import Rat
from spaceship.action import commands
'''Test map with key handling functionality to test player input in controlled layouts'''

test_map_path = "./assets/maps/test_map.png"

def main():
    rat = Rat(33, 11)
    cave = Cave(66, 22)
    t.open()
    while True:
        t.clear()
        cave.fov_calc([(rat.x, rat.y, rat.sight)])
        for x, y, col, char in cave.output(rat.x, rat.y):
            t.puts(x, y, "[c={}]{}[/c]".format(col, char))
        t.refresh()
        k = t.read()
        if k in (t.TK_UP, t.TK_DOWN, t.TK_LEFT, t.TK_RIGHT):
            if not t.state(t.TK_SHIFT):
                x, y, a, act = commands[(k, 0)]
                rat.move(x, y)
        else:
            break
        
if __name__ == "__main__":
    main()