# coding=utf-8

from bearlibterminal import terminal as term
from ctypes import c_uint32, addressof
from namedlist import namedlist
from random import randint
from time import time, sleep
from tools import bresenhams

maxi_x, maxi_y = 80, 24
limit_x, limit_y = 78, 28 # offset by -1 to account for start index 0
factor_x, factor_y = 2, 1
window_size = (limit_x+factor_x*2, limit_y+factor_y*2) # add the offset back to create window size with start index 1

def test_line():
    term.composition(True)
    global cursor_pos
    term.set("U+E000: ./assets/transport.png, resize=32x32")
    proceed = True
    while proceed:
        term.clear()
        start = (randint(0, maxi_x), randint(0, maxi_y))
        end = (randint(0, maxi_x), randint(0, maxi_y))

        points = bresenhams(start, end)
        for x, y in points:
            term.puts(x, y, '.')
        term.refresh()
        sleep(3)
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
            else:
                term.puts(0,6, 'other input')

if __name__ == "__main__":
    term.open()
    x, y = window_size
    term.set("window: size={}x{}, title='Animation Test'".format(x, y))
    test_line()
    term.close