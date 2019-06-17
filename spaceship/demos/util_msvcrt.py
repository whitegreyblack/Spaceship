# util_msvcrt.py

"""Defines keybindings from msvcrt library"""

import msvcrt

moveset = {
    b'\xe0': {
        b'H': (0, -1), # down
        b'P': (0, 1), # up
        b'K': (-1, 0), # left
        b'M': (1, 0) # right
    }
}
