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
        term.TK_1: (-1, 1),
        term.TK_2: (0, 1),
        term.TK_3: (1, 1),
        term.TK_4: (-1, 0),
        term.TK_5: (0, 0),
        term.TK_6: (1, 0),
        term.TK_7: (-1, -1),
        term.TK_8: (0, -1),
        term.TK_9: (1, -1),
    }