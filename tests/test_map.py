import os
import sys
import time
import timeit
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))+'/../')
from bearlibterminal import terminal as t
from spaceship.classes.city import City
from spaceship.classes.cave import Cave
from spaceship.classes.monsters import Rat
from spaceship.classes.bat import Bat
from spaceship.action import commands
'''Test map with key handling functionality to test player input in controlled 
layouts
'''
test_map_path = "./assets/maps/test_map.png"

def test_map_output_speed_with_yield():
    def run():
        cave.fov_calc([(bat.x, bat.y, bat.sight)])
        for _ in cave.output(bat.x, bat.y):
            pass

    cave = Cave(66, 22)
    bat = Bat(15, 10)
    cave.units_add([bat])

    t = timeit.timeit(run, number=1000)
    return t

def test_map_output_speed_with_return():
    def run():
        cave.fov_calc([(bat.x, bat.y, bat.sight)])
        for _ in cave.output_return(bat.x, bat.y):
            pass

    cave = Cave(66, 22)
    bat = Bat(15, 10)
    cave.units_add([bat])

    t = timeit.timeit(run, number=1000)
    return t

def run_sample_map_with_units():
    bat = Bat(15, 10)
    rat = Rat(33, 11)
    cave = Cave(66, 22)
    cave.units_add([bat, rat])
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

def test_map_unit_iteration():
    cave = Cave(66, 22, generate=False)
    cave.units_add([Bat(15, 10)])
    assert len(list(cave.units)) == 1
    
def test_map_unit_build_dictionary():
    b = Bat(15, 10)
    cave = Cave(66, 22, generate=False)
    cave.units_add([b])
    assert {u.position: u for u in cave.units} == {b.position: b}

def test_map_unit_position_iteration():
    cave = Cave(66, 22, generate=False)
    cave.units_add([Bat(15, 10)])
    assert list(cave.unit_positions) == [(15, 10)]

def test_map_unit_position_at():
    b = Bat(15, 10)
    cave = Cave(66, 22, generate=False)
    cave.units_add([b])
    assert cave.unit_at_position(15, 10) == b    

if __name__ == "__main__":
    # test_sample_map_with_units()
    # print(sum([test_map_output_speed_with_yield() for i in range(5)]) / 5)
    # print(sum([test_map_output_speed_with_return() for i in range(5)]) / 5)

    # test_map_unit_iteration()
    # test_map_unit_position_iteration()
    pass