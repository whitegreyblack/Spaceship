# -*- coding=utf-8 -*-
"""Movement.py covers key-value pairs in bearlibterminal associated with movement actions. \
Key constants are seperated into two lists to differentiate between arrow and numpad keys. \
The key-value pair matches a bearlibterminal key to a two element tuple determining x, y directions"""

"""
TODO: Might combine the movement keys into one dictionary
      Rename filename into actions.py with movement as a sub category in the file
      Add action key-value dictionaries alongside a combined movement dictionary
"""
from collections import namedtuple
from bearlibterminal import terminal as term
"""
    Movement:
        <,^,v,>: Movement keys -> (x,y)
    Actions:
        (O|o)pen (blockable(s)): -> unblockable(s)
        (C|c)lose (unblockable(s)): -> blockable(s)
        (T|t)alk (object(s)): -> string
    Menu Screens:
        (I|i)nventory (menu): -> inventory screen
        (Esc|Escape) (menu): -> escape screen/main menu
"""
keypress = namedtuple("Keypress", "x y char action")

# handles processing input into keypress commands for player
commands_player = {
    (term.TK_UP, 0): keypress(0, -1, None, "move"),
    (term.TK_DOWN, 0): keypress(0, 1, None, "move"),
    (term.TK_LEFT, 0): keypress(-1, 0, None, "move"),
    (term.TK_RIGHT, 0): keypress(1, 0, None, "move"),
    (term.TK_KP_1, 0): keypress(-1, 1, None, "move"),
    (term.TK_KP_2, 0): keypress(0, 1, None, "move"),
    (term.TK_KP_3, 0): keypress(1, 1, None, "move"),
    (term.TK_KP_4, 0): keypress(-1, 0, None, "move"),
    (term.TK_KP_5, 0): keypress(0, 0, None, "move"),
    (term.TK_KP_6, 0): keypress(1, 0, None, "move"),
    (term.TK_KP_7, 0): keypress(-1, -1, None, "move"),
    (term.TK_KP_8, 0): keypress(0, -1, None, "move"),
    (term.TK_KP_9, 0): keypress(1, -1, None, "move"),

    (term.TK_A, 0): keypress(None, None, "a", "attack"),
    (term.TK_O, 0): keypress(None, None, "o", "open"),
    (term.TK_C, 0): keypress(None, None, "c", "close"),
    (term.TK_T, 0): keypress(None, None, "t", "talk"),
    (term.TK_I, 0): keypress(None, None, "v", "inventory"),
    (term.TK_Q, 0): keypress(None, None, "q", "equipment"),
    (term.TK_D, 0): keypress(None, None, "d", "drop"),
    (term.TK_U, 0): keypress(None, None, "u", "use"),
    (term.TK_E, 0): keypress(None, None, "e", "eat"),
    (term.TK_COMMA, 0): keypress(None, None, ",", "pickup"),
    (term.TK_I, 0): keypress(None, None, "i", "equipment"),
    (term.TK_V, 0): keypress(None, None, "v", "inventory"),
    # (term.TK_2, 1): keypress(None, None, "@", "profile"),
    (term.TK_S, 1): keypress(None, None, "S", "save"),
    (term.TK_COMMA, 1): keypress(None, None, "<", "exit"),
    (term.TK_PERIOD, 1): keypress(None, None, ">", "enter"),
}

# handles processing ai 'input' into keypress commands
commands_ai = {
    'wait': keypress(0, 0, None, "move"),
    'move': {
        (-1, -1): keypress(-1, -1, None, "move"),
        ( 0, -1): keypress(0, -1, None, "move"),
        ( 1, -1): keypress(1, -1, None, "move"),
        ( 1,  0): keypress(1, 0, None, "move"),
        ( 1,  1): keypress(1, 1, None, "move"),
        ( 0,  1): keypress(0, 1, None, "move"),
        ( -1, 1): keypress(-1, 1, None, "move"),
        ( -1, 0): keypress(-1, 0, None, "move"),
    }
}

if __name__ == "__main__":
    for i in keys:
        print(keys)
