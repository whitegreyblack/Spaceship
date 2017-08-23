# -*- coding=utf-8 -*-

from bearlibterminal import terminal as term
from ctypes import c_uint32, addressof
from namedlist import namedlist
from time import time

limit_x, limit_y = 76, 20 # offset by -1 to account for start index 0
factor_x, factor_y = 1, 1
window_size = (limit_x+factor_x, limit_y+factor_y) # add the offset back to create window size with start index 1
player_pos = (10, 7)
movement_ratio = (factor_x, factor_y)
movement_costs = {
    term.TK_LEFT: (-1, 0),
    term.TK_RIGHT: (1, 0),
    term.TK_DOWN: (0, 1),
    term.TK_UP: (0, -1),
}

wmap = """\
####################
#                  #
#                  #
#    #        #    #
#                  #
#                  #
#                  #
#                  #
#    #        #    #
#                  #
#                  #
####################
"""

def movement(pos, change, factor, low, high):
    updated = pos + change * factor
    return updated if low < updated < high else max(low, min(updated, high))

def test_map():
    term.composition(True)
    global player_pos
    term.set("U+E003: ./assets/cursor03_small.png")
    term.clear()
    term.refresh()
    proceed = True
    blockables = [(5,4), (5, 9), (14, 4), (14, 9)]
    try:
        while proceed:
            term.clear()
            term.puts(0, 0, 'Animating a map\n')
            x, y = player_pos
            term.puts(0, 1, wmap)
            term.puts(x, y, '@')
            while proceed and term.has_input():
                term.puts(21, 5, 'Got input')
                code = term.read()
                if code in (term.TK_ESCAPE, term.TK_CLOSE):
                    term.clear()
                    term.puts(10, 6, 'Really Quit? (Y/N)')
                    term.refresh()
                    code = term.read()
                    if code in (term.TK_Y,):
                        proceed = False
                elif code in movement_costs.keys():
                    tx, ty = x, y
                    dx, dy = movement_costs[code]
                    fx, fy = movement_ratio
                    x = movement(x, dx, fx, 1, 18)
                    y = movement(y, dy, fy, 2, 11)
                    if (x, y) in blockables:
                        x, y = tx, ty
                    player_pos = (x, y)
                else:
                    term.puts(0,6, 'other input')
            term.refresh()
    except KeyboardInterrupt:
        pass

if __name__ == "__main__":
    term.open()
    x, y = window_size
    term.set("window: size={}x{}, title='Animation Test'".format(x, y))
    test_map()
    term.close