# main implementation of core mechanics
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))+'/../')
from spaceship.gamelog import GameLogger
from spaceship.tools import bresenhams, deltanorm, movement
from spaceship.action import key_movement, num_movement, key_actions, action, keypress
from spaceship.objects import Map, Object
from bearlibterminal import terminal as term
from collections import namedtuple
from namedlist import namedlist
from maps import stringify, hextup, hexone
from random import randint, choice
from time import clock
from spaceship.constants import SCREEN_HEIGHT, SCREEN_WIDTH
# LIMIT_FPS = 30 -- later used in sprite implementation
blocked = []
dungeon = Map(stringify("./assets/testmap_colored.png"))

# ---------------------------------------------------------------------------------------------------------------------#
# TERMINAL SETUP & IMAGE IMPORTS


def setup():
    term.open()
    term.set(
        "window: size={}x{}, cellsize={}x{}, title='Main Game'".format(
            SCREEN_WIDTH,
            SCREEN_HEIGHT,
            8, 12))

# END SETUP TOOLS
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
    else:
        print("unrecognized command")
    return keydown(x, y, act)

# should change to movement process
walkBlock = "walked into {}"
def key_process(x, y, action, unit, blockables):

    global player, glog
    unit_pos = [(unit.x, unit.y) for unit in units]

    outofbounds = 0 <= player.x + x < len(blockables[0]) \
        and 0 <= player.y + y < len(blockables)

    occupied = (player.x + x, player.y + y) in unit_pos

    try:
        blocked = blockables[player.y + y][player.x + x]
        ch = dungeon.square(player.x+x, player.y+y)
    except BaseException:
        blocked = False

    if not (blocked or occupied or not outofbounds):
        player.move(x, y)
    else:
        if blocked:
            if ch == "+":
                glog.add(walkBlock.format("a door"))
            if ch == "#":
                glog.add(walkBlock.format("a wall"))
                glog.add(f"{player.x+x}, {player.y+y}")
        elif occupied:
            glog.add(walkBlock.format("someone"))
        elif outofbounds:
            glog.add(walkBlock.format("the edge of the map"))

    for unit in units:
   #     if unit.c != "grey":
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

def openInventory(x, y, key):
    glog.add("opeining inventory")
    playscreen = False

    current_range = 0
    while True:
        term.clear()
        log_screen()
        term.puts(2, 1, "[color=white]Inventory")
        term.refresh()
        code = term.read()
        if code in (term.TK_ESCAPE, term.TK_I,):
            break
        elif code == term.TK_UP:
            if current_range > 0: current_range -= 1
        elif code == term.TK_DOWN:
            if current_range < 10: current_range += 1
    else:
        glog.add("Closing inventoryy")
    term.clear()
    log_screen()
    map_screen()

def onlyOne(container):
    return len(container) == 1

def eightsquare(x, y):
    space = namedtuple("Space", ("x","y"))
    return [space(x+i,y+j) for i, j in list(num_movement.values())]

def interactDoor(x, y, key):
    def openDoor(i, j):
        glog.add("Opened door")
        dungeon.open_door(i, j)
        dungeon.unblock(i, j)

    def closeDoor(i, j):
        glog.add("Closed door")
        dungeon.close_door(i, j)
        dungeon.reblock(i, j)

    opening = key is "o"
    char = "+" if key is "o" else "/"

    reachables = []
    for i, j in eightsquare(x, y):
        if (i, j) != (x, y):
            if dungeon.square(i, j) is char:
                reachables.append((i,j))

    if not reachables:
        glog.add("No {} near you".format("openables" if opening else "closeables"))
    
    elif onlyOne(reachables):
        i, j = reachables.pop()
        openDoor(i, j) if opening else closeDoor(i, j)

    else:
        term.clear()
        glog.add("Which direction?")
        log_screen()
        map_screen()
        term.refresh()
        code = term.read()

        if code in key_movement:
            cx, cy = key_movement[code]
        elif code in num_movement:
            cx, cy = num_movement[code]
        else:
            return

        if (x+cx, y+cy) in reachables:
            openDoor(x+cx, y+cy) if opening else closeDoor(x+cx, y+cy)

actions={
    'o': interactDoor,
    'c': interactDoor,
    'i': openInventory,
    'f1': dungeon.sundown,
    'f2': dungeon.sunup,
}

def processAction(x, y, key):                        
    try:
        actions[key](x, y, key)
    except TypeError:
        actions[key]()
    except KeyError:
        print("unknown command")
            

# End Movement Functions
# ---------------------------------------------------------------------------------------------------------------------#
# Graphic functions
def draw():
    global COLOR_DARK_GROUND, COLOR_DARK_WALL

    for unit in units:
        x, y, i, c = unit.draw()
        term.puts(x, y, ('[color={}]' + i + '[/color]').format(c))

def log_screen():
    messages = glog.write().messages
    if messages:
        for idx in range(len(messages)):
            term.puts(0, SCREEN_HEIGHT-4+idx, messages[idx])

def map_screen():
    """ Logic:
            Should first print map in gray/black
            Then print units/interactables?
            Finally light sources and player?"""
    for x, y, lit, ch in list(dungeon.output(player.x, player.y, units)):
        # term.bkcolor(bgkd)
        term.puts(x, y, "[color={}]{}[/color]".format(lit, ch))
    term.refresh()

# End graphics functions
# ---------------------------------------------------------------------------------------------------------------------#
# Start initializations

setup()
glog = GameLogger()
# global game variables
FOV_RADIUS = 10
#MAP_WIDTH, MAP_HEIGHT = 24, 48

MAP_FACTOR = 2
COLOR_DARK_WALL = term.color_from_argb(128, 0, 0, 100)
COLOR_DARK_GROUND = term.color_from_argb(128, 50, 50, 150)
#px, py = SCREEN_WIDTH//2, SCREEN_HEIGHT//2
px, py = 86, 30
#px, py = 0, 0
# units = Map.appendUnitList("./unitlist/test_map_colored.png")
# map = Map(parse("testmap.dat"))
#dungeon = Map(stringify("./assets/testmap.png"))
player = Object(px, py, '@')
npc = Object(7, 7, '@', 'orange')
npc1 = Object(5, 15, '@', 'orange')
npc2 = Object(0, 56, '@', 'orange')
guard3 = Object(77, 11, '@', 'orange')
guard1 = Object(77, 12, "@", 'orange')
guard2 = Object(77, 17, "@", 'orange')
guard4 = Object(67, 17, '@', 'orange')
units = [npc, guard1, guard2, guard3, guard4, npc1, npc2]
proceed = True
lr = 5
lights = [
    (64, 13, lr),
#    (72, 13, lr),
    (79, 13, lr),
#    (86, 13, lr),
#    (98, 13, lr),
    (103, 13, lr),
#    (110, 13, lr),
]
while proceed:
    term.clear()
    log_screen()
    dungeon.fov_calc(lights+[(player.x, player.y, FOV_RADIUS)])
    # removed list creation
    #positions = [(x, y, lit, ch)
    #             for x, y, lit, ch in dungeon.output(player.x, player.y, units)]
    map_screen()
    x, y, a = key_in()
    if a:
        processAction(player.x, player.y, a)
    else:
        key_process(x, y, None, [], dungeon.block)
    # while term.has_input():
    #     term.read()
        #processAction(player.x, player.y, action("o","open"), [], dungeon.block)
    #term.refresh()
    #print(clock()-t1)
# End Initiailiation
# ---------------------------------------------------------------------------------------------------------------------#
