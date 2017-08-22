# coding=utf-8

from bearlibterminal import terminal as term
from ctypes import c_uint32, addressof
from namedlist import namedlist
from time import time

limit_x, limit_y = 76, 20 # offset by -1 to account for start index 0
factor_x, factor_y = 4, 2
window_size = (limit_x+factor_x, limit_y+factor_y) # add the offset back to create window size with start index 1
cursor_pos = (20, 6)
movement_ratio = (factor_x, factor_y)
movement_costs = {
    term.TK_LEFT: (-1, 0),
    term.TK_RIGHT: (1, 0),
    term.TK_DOWN: (0, 1),
    term.TK_UP: (0, -1),
}

def test_sprite():
    global cursor_pos
    term.set("U+E000: ./assets/cursor01.png")
    term.set("U+E001: ./assets/cursor02.png")
    term.set("U+E002: ./assets/cursor03.png")
    term.set("U+E003: ./assets/cursor03_small.png")
    term.set("U+E004: ./assets/cursor03_smaller.png")
    term.clear()
    term.refresh()
    proceed = True
    try:
        while proceed:
            term.clear()
            term.puts(0, 0, 'Animating a cursor\n')
            x, y = cursor_pos
            term.put(x, y, 57347)
            term.puts(0, 1, f'{x}')
            term.puts(3, 1, f'{y}')
            term.puts(7, 1, f'{x//factor_x}')
            term.puts(10, 1, f'{y//factor_y}')
            term.put(5,5, 'a')
            while proceed and term.has_input():
                term.puts(0, 5, 'Got input')
                code = term.read()
                if code in (term.TK_ESCAPE, term.TK_CLOSE):
                    term.clear()
                    term.puts(0, 1, 'Really Quit? (Y/N)')
                    term.refresh()
                    code = term.read()
                    if code in (term.TK_Y, ):
                        proceed = False
                elif code in movement_costs.keys():
                    dx, dy = movement_costs[code]
                    fx, fy = movement_ratio
                    if 0 < x + dx*fx < limit_x:
                        x += dx*fx
                    else:
                        x = max(min(x+dx*fx, limit_x), 0)

                    if 0 < y + dy*fy < limit_y:
                        y += dy*fy
                    else:
                        y = max(min(y+dy*fy, limit_y), 0)
                    cursor_pos = (x, y)
                else:
                    term.puts(0,6, 'other input')
            term.refresh()
    except KeyboardInterrupt:
        pass

if __name__ == "__main__":
    term.open()
    x, y = window_size
    term.set("window: size={}x{}, title='Animation Test'".format(x, y))
    test_sprite()
    term.close