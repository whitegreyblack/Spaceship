# main implementation of core mechanics
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))+'/../')
from spaceship.gamelog import GameLogger
from spaceship.tools import bresenhams, deltanorm, movement
from spaceship.action import key_movement, num_movement, key_actions, action, keypress
from spaceship.objects import Map, Object, Tile
from bearlibterminal import terminal as term
from collections import namedtuple
from namedlist import namedlist
from maps import stringify, hextup, hexone
from random import randint, choice
from spaceship.constants import SCREEN_HEIGHT, SCREEN_WIDTH
# LIMIT_FPS = 30 -- later used in sprite implementation
blocked = []

# ---------------------------------------------------------------------------------------------------------------------#
# TERMINAL SETUP & IMAGE IMPORTS


def setup():
    term.open()
    term.set(
        "window: size={}x{}, cellsize={}x{}, title='Main Game'".format(
            SCREEN_WIDTH,
            SCREEN_HEIGHT,
            8,16))
# ---------------------------------------------------------------------------------------------------------------------#

# ---------------------------------------------------------------------------------------------------------------------#
# Keyboard input


def key_in():
    keydown = namedtuple("Key_Down", ("x", "y", "a"))
    global proceed
    # movement
    code = term.read()
    if code in (term.TK_ESCAPE, term.TK_CLOSE):
        proceed = False
    act, x, y = 0, 0, 0
    if code in key_movement:
        x, y = key_movement[code]
    elif code in num_movement:
        x, y = num_movement[code]
    elif code in key_actions:
        act = key_actions[code].key
        print(act)
    else:
        print("unrecognized command")
    return keydown(x, y, act)

# should change to movement process
def key_process(x, y, action, unit, blockables):
    global player, glog
    unit_pos = [(unit.x, unit.y) for unit in units]

    outofbounds = 0 <= player.x + x < len(blockables[0]) \
        and 0 <= player.y + y < len(blockables)

    occupied = (player.x + x, player.y + y) in unit_pos

    try:
        blocked = blockables[player.y + y][player.x + x]
    except BaseException:
        blocked = False

    if not (blocked or occupied or not outofbounds):
        player.move(x, y)
    else:
        if blocked:
            glog.add("Walked into a wall")
        # if blocked:
        #     term.puts(0, MAP_HEIGHT - 2, "wall")
        # if occupied:
        #     term.puts(5, MAP_HEIGHT - 2, "occupied")
        # term.refresh()

    for unit in units:
        if unit.c != "grey":
            x, y = 0, 0
            if randint(0, 1):
                x, y = num_movement[choice(list(num_movement.keys()))]
            try:
                blocked = blockables[unit.y+y][unit.x+x]
            except:
                blocked = False
            occupied = (unit.x + x, unit.y + y) in unit_pos or (unit.x+x, unit.y+y) == (player.x, player.y)
            outofbounds = 0 <= unit.x + x < len(blockables[0]) and 0 <= unit.y + y < len(blockables)
            if not (blocked or occupied or not outofbounds):
                unit.move(x, y)

def onlyOne(container):
    return len(container) == 1

def eightsquare(x, y):
    space = namedtuple("Space", ("x","y"))
    return [space(x+i,y+j) for i, j in list(num_movement.values())]

def actionOpen(x, y):
    def openDoor(openable):
        i, j = openable
        dungeon.open_door(i, j)
        dungeon.unblock(i, j)

    glog.add("open action")
    openables = []
    for i, j in eightsquare(x, y):
        if (i, j) != (x, y):
            if dungeon.square(i, j) == "+":
                glog.add("openable object near you")
                openables.append((i, j))
    if not openables:
        print("no openables near you")
        glog.add("No openables near you")
    elif onlyOne(openables):
        openDoor(openables[0])
    else:
        glog.add("Which direction?")
        code = term.read()
        if code in key_movement:
            cx, cy = key_movement[code]
        elif code in num_movement:
            cx, cy = num_movement[code]
        else:
            return
        if (x+cx, y+cy) in openables:
            openDoor((x+cx, y+cy))        

def actionClose(x, y):
    pass

actions={
    'o': actionOpen,
    'c': actionClose,
}

def processAction(x, y, key, unit, blockables):
    global player, glog
            

            
    print(x, y, key)
            
    try:
        actions[key](x, y)
    except KeyError:
        print("unknown command")
    """
    if action == "o":
        print(action)
        print("open action")
        openables = []
        for i, j in eightsquare(x, y):
            if (i, j) != (x, y):
                if dungeon.square(i, j) == "+":
                    print("there is an openable object near you")
                    openables.append((i, j))
        open_door(openables)
    if action == "c":
        print(action, "closing")
        closeables = []
        for i, j in eightsquare(x, y):
            if (i, j) != (x, y):
                if dungeon.square(i, j) == "/":
                    print("there is a closeable object near you")
                    closeables.append((i, j))
        if len(closeables) == 1:
            i, j = closeables[0]
            dungeon.close_door(i, j)
            dungeon.reblock(i, j)
    #print(eightsquare(x,y))
    """
            

# End Movement Functions
# ---------------------------------------------------------------------------------------------------------------------#


# ---------------------------------------------------------------------------------------------------------------------#
# Map functions

# End map functions
# ---------------------------------------------------------------------------------------------------------------------#

# ---------------------------------------------------------------------------------------------------------------------#
# Graphic functions
def draw():
    global COLOR_DARK_GROUND, COLOR_DARK_WALL

    for unit in units:
        x, y, i, c = unit.draw()
        term.puts(x, y, ('[color={}]' + i + '[/color]').format(c))

# End graphics functions
# ---------------------------------------------------------------------------------------------------------------------#


# ---------------------------------------------------------------------------------------------------------------------#
# Start initializations
setup()
glog = GameLogger()
# global game variables
FOV_RADIUS = 25
MAP_WIDTH, MAP_HEIGHT = 24, 48
MAP_FACTOR = 2
COLOR_DARK_WALL = term.color_from_argb(128, 0, 0, 100)
COLOR_DARK_GROUND = term.color_from_argb(128, 50, 50, 150)
#px, py = SCREEN_WIDTH//2, SCREEN_HEIGHT//2
px, py = 14, 4
dungeon = Map(stringify("./assets/testmap_colored.png"))
#dungeon = Map(stringify("./assets/testmap.png"))
player = Object(px, py, '@')
npc = Object(7, 7, '@', 'orange')
npc1 = Object(5, 15, '@', 'orange')
npc2 = Object(16, 5, '@', 'orange')
guard3 = Object(77, 11, '@', 'grey')
guard1 = Object(77, 12, "@", 'grey')
guard2 = Object(77, 17, "@", 'grey')
guard4 = Object(67, 17, '@', 'grey')
units = [npc, guard1, guard2, guard3, guard4, npc1, npc2]
proceed = True


while proceed:
    term.clear()
    message_index = 0
    messages = glog.write().messages
    print(messages)
    if messages:
        for message in messages:
            print(message)
            term.puts(0, SCREEN_HEIGHT-5+message_index, message)
            message_index += 1
    dungeon.fov_calc(player.x, player.y, FOV_RADIUS)
    # removed list creation
    #positions = [(x, y, lit, ch)
    #             for x, y, lit, ch in dungeon.output(player.x, player.y, units)]
    for x, y, lit, ch in list(dungeon.output(player.x, player.y, units)):
        term.puts(x, y, "[color={}]{}[/color]".format(lit, ch))
        term.puts(0, SCREEN_HEIGHT-1, "{} {}".format(player.x, player.y))
    term.refresh()
    x, y, a = key_in()
    if a:
        processAction(player.x, player.y, a, [], dungeon.block)
    else:
        key_process(x, y, None, [], dungeon.block)
        #processAction(player.x, player.y, action("o","open"), [], dungeon.block)
    term.refresh()

# End Initiailiation
# ---------------------------------------------------------------------------------------------------------------------#
