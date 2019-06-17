# util_curses.py

"""Defines keybindings from curses library"""

import curses

moveset = {
    curses.KEY_DOWN: (0, 1), # 258
    curses.KEY_UP: (0, -1), # 259
    curses.KEY_LEFT: (-1, 0), # 260
    curses.KEY_RIGHT: (1, 0), # 261
}
