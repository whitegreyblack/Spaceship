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
    
keypress = namedtuple("Keypress", ("x", "y"))
movement = namedtuple("Movement", ("x", "y"))
action = namedtuple("Action", ("key", "action"))

key_movement={
    term.TK_UP: movement(0, -1),
    term.TK_DOWN: movement(0, 1),
    term.TK_LEFT: movement(-1, 0),
    term.TK_RIGHT: movement(1, 0),
}
num_movement={
    term.TK_KP_1: movement(-1, 1),
    term.TK_KP_2: movement(0, 1),
    term.TK_KP_3: movement(1, 1),
    term.TK_KP_4: movement(-1, 0),
    term.TK_KP_5: movement(0, 0),
    term.TK_KP_6: movement(1, 0),
    term.TK_KP_7: movement(-1, -1),
    term.TK_KP_8: movement(0, -1),
    term.TK_KP_9: movement(1, -1),
}

# Open|Close -> Openable/Closable classes? --> Doors/Chests/Hatch?
key_actions={
    term.TK_A: action("a", "attack"),
    term.TK_O: action("o", "open"),
    term.TK_C: action("c", "close"),
    term.TK_T: action("t", "talk"),
    term.TK_I: action("i", "inventory"),
    term.TK_F1: action("f1", "func_key"),
    term.TK_F2: action("f2", "func_key"),
    term.TK_COMMA: action(",", "pickup"),
    term.TK_PERIOD: action(">", "enter"),
    term.TK_COMMA: action("<", "exit"),
}

world_key_actions = {
    term.TK_PERIOD: action(">", "enter"),
    term.TK_COMMA: action("<", "exit"),
}

if __name__ == "__main__":
    for i in world_key_actions.keys():
        print(i)