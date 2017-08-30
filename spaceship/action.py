# -*- coding=utf-8 -*-
"""Movement.py covers key-value pairs in bearlibterminal associated with movement actions. \
Key constants are seperated into two lists to differentiate between arrow and numpad keys. \
The key-value pair matches a bearlibterminal key to a two element tuple determining x, y directions"""

"""
TODO: Might combine the movement keys into one dictionary
      Rename filename into actions.py with movement as a sub category in the file
      Add action key-value dictionaries alongside a combined movement dictionary
"""
from bearlibterminal import terminal as term
key_movement={
        term.TK_UP: (0, -1),
        term.TK_DOWN: (0, 1),
        term.TK_LEFT: (-1, 0),
        term.TK_RIGHT: (1, 0),
    }
num_movement={
        term.TK_KP_1: (-1, 1),
        term.TK_KP_2: (0, 1),
        term.TK_KP_3: (1, 1),
        term.TK_KP_4: (-1, 0),
        term.TK_KP_5: (0, 0),
        term.TK_KP_6: (1, 0),
        term.TK_KP_7: (-1, -1),
        term.TK_KP_8: (0, -1),
        term.TK_KP_9: (1, -1),
    }
