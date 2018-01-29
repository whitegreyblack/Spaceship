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
from spaceship.classes.point import spaces, Point
import spaceship.strings as strings
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
    (term.TK_L, 0): keypress(None, None, "l", "look"),
    (term.TK_COMMA, 0): keypress(None, None, ",", "pickup"),
    (term.TK_I, 0): keypress(None, None, "i", "equipment"),
    (term.TK_V, 0): keypress(None, None, "v", "inventory"),
    (term.TK_T, 1): keypress(None, None, "T", "throw"),
    (term.TK_Z, 0): keypress(None, None, "z", "zap"),
    (term.TK_S, 0): keypress(None, None, "s", "spells"),
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

def go_down_stairs(unit, area, area_constructor):
    '''Go Down command: Checks player position to the downstairs position
    in the current location. If they match then create a dungeon with the
    player starting position at the upstairs of the new location
    '''
    log = "You cannot go downstairs without stairs."

    if unit.local == area.stairs_down:
        if not area.sublevel:
            area.sublevel = area_constructor(width=area.width,
                                             height=area.height,
                                             max_rooms=18)
            area.sublevel.parent = area

        area.unit_remove(unit)
        area = area.sublevel
        area.units_add([unit])
        unit.descend()
        unit.local = Point(area.stairs_up)
        log = "You go down the stairs."

    return unit, area, [log]

def go_up_stairs(unit, area, maptypes):
    '''Go Up command: Checks player position to the upstairs position
    in the current location. Then determine the parent location 
    and reset position according to the type of parent
    '''
    log = "You cannot go upstairs without stairs."
    ascend = False

    if area.map_type == maptypes.CAVE:
        # Every child map has a parent map
        if unit.local == area.stairs_up:
            ascend = True
            log = "You go up the stairs."

    elif area.map_type in (maptypes.CITY, maptypes.WILD):
        ascend = True
        log = "You begin travelling."

    if ascend:
        area.unit_remove(unit)
        area = area.parent
        area.units_add([unit])
        unit.ascend()  

    return unit, area, [log]

def close_door(unit, area, logger):
    '''Close door command: handles closing doors in a one unit distance
    from the player. Cases can range from no doors, single door, multiple 
    doors, with multiple doors asking for input direction
    '''
    log = ""
    doors = []
    door = None

    for point in spaces(unit.local):
        if point != unit.local and area.square(*point).char == '/':
            doors.append(point)

    if not doors:
        log = strings.close_door_none
    elif len(doors) == 1:
        door = doors.pop()
    else:
        logger(strings.close_door_many)
        code = term.read()
        shifted = term.state(term.TK_SHIFT)

        try:
            dx, dy, _, act = commands_player[(code, shifted)]
        except KeyError:
            log = strings.close_door_invalid
        else:
            if act == "move" and unit.local + Point(dx, dy) in doors:
                door = unit.local + Point(dx, dy)
            else:
                log = strings.close_door_error
        
    if door:
        area.close_door(*door)
        log = strings.close_door_act

    return area, [log]

def open_door(unit, area, logger):
    '''Open door command: handles opening doors in a one unit distance from
    the player. Cases can range from no doors, single door, multiple 
    doors, with multiple doors asking for input direction
    '''
    log = ""
    doors = []
    door = None

    for point in spaces(unit.local):
        if point != unit.local and area.square(*point).char == '+':
            doors.append(point)    
    
    if not doors:
        log = strings.open_door_none
    elif len(doors) == 1:
        door = doors.pop()
    else:
        logger(strings.open_door_many)
        code = term.read()
        shifted = term.state(term.TK_SHIFT)

        try:
            dx, dy, _, act = commands_player[(code, shifted)]
        except KeyError:
            log = strings.open_door_invalid
        else:
            if act == "move" and unit.local + Point(dx, dy) in doors:
                door = unit.local + Point(dx, dy)
            else:
                log = strings.open_door_error
        
    if door:
        area.open_door(*door)
        log = strings.open_door_act      
    
    return area, [log]

def converse(unit, area, logger):
    '''Converse action: handles finding units surrounding the given unit and 
    talks to them. Cases can range from no units, a single unit, and multiple
    units, with multiple units asking for input direction.
    '''
    log = ""
    units = []
    other = None

    for point in spaces(unit.local):
        if point != unit.local and area.unit_at(*point):
            units.append(point)

    if not units:
        log = strings.converse_none
    elif len(units) == 1:
        other = units.pop()
    else:
        logger(strings.converse_many)
        code = term.read()
        shifted = term.state(term.TK_SHIFT)

        try:
            dx, dy, _, act = commands_player[(code, shifted)]
        except KeyError:
            log = strings.converse_invalid
        else:
            if act == "move" and unit.local + Point(dx, dy) in doors:
                other = unit.local + Point(dx, dy)
            else:
                log = strings.converse_error
    
    if unit:
        log = area.unit_at(*other).talk()
    
    return [log]