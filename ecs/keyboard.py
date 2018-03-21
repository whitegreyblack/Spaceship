# keyboard.py
from bearlibterminal import terminal as term

class Keyboard:
    UP, DOWN, LEFT, RIGHT = term.TK_UP, term.TK_DOWN, term.TK_LEFT, term.TK_RIGHT
    ESCAPE = term.TK_ESCAPE
    ARROWS = {
        term.TK_UP: (0, -1),
        term.TK_DOWN: (0, 1), 
        term.TK_LEFT: (-1, 0), 
        term.TK_RIGHT: (1, 0),
    }
    KEYPAD = {
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
    KEYBOARD = {
        (term.TK_COMMA, 0): "pickup",
        (term.TK_I, 0): "inventory",
        (term.TK_D, 0): "drop",
        (term.TK_E, 0): "equip",
        (term.TK_U, 0): "unequip",
        (term.TK_B, 0): "backpack",
    }
    MAIN_MENU = {
        term.TK_P: "pressed play",
        term.TK_E: "pressed exit",
    }