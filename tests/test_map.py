import os
import sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))+'/../')
from bearlibterminal import terminal as t
from spaceship.maps.city import City
from spaceship.maps.cave import Cave
from spaceship.units.monsters import Rat, Bat
from spaceship.action import commands
'''Test map with key handling functionality to test player input in controlled layouts'''

test_map_path = "./assets/maps/test_map.png"

def main():
    bat = Bat(15, 10)
    rat = Rat(33, 11)
    cave = Cave(66, 22)
    cave.add_units([bat, rat])
    t.open()
    proceed=True
    while proceed:
        for unit in [bat, rat]:
            t.clear()
            cave.fov_calc([(unit.x, unit.y, unit.sight)])
            for x, y, col, char in cave.output(unit.x, unit.y):
                t.puts(x, y, "[c={}]{}[/c]".format(col, char))
            t.refresh()

            k = t.read()
            if k in (t.TK_UP, t.TK_DOWN, t.TK_LEFT, t.TK_RIGHT, t.TK_KP_5):
                if not t.state(t.TK_SHIFT):
                    x, y, a, act = commands[(k, 0)]
                    unit.move(x, y)
            else:
                proceed=False
                break

if __name__ == "__main__":
    main()