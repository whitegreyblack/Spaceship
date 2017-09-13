# main implementation of core mechanics
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))+'/../')
from spaceship.gamelog import GameLogger
from spaceship.tools import bresenhams, deltanorm, movement
from spaceship.action import key_movement, num_movement, key_actions, action, keypress
from spaceship.objects import Map, Object, Person
from bearlibterminal import terminal as term
from collections import namedtuple
from namedlist import namedlist
from maps import stringify, hextup, hexone, toInt
from random import randint, choice
from time import clock
from spaceship.constants import SCREEN_HEIGHT, SCREEN_WIDTH, FOV_RADIUS
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
            8, 8))

# END SETUP TOOLS
# ---------------------------------------------------------------------------------------------------------------------#
# Keyboard input


def key_in():
    keydown = namedtuple("Key_Down", ("x", "y", "a"))
    global proceed
    # movement
    act, x, y = 0, 0, 0
    code = term.read()
    if code in (term.TK_ESCAPE, term.TK_CLOSE):
        glog.dumps()
        proceed = False
    elif code in key_movement:
        x, y = key_movement[code]
    elif code in num_movement:
        x, y = num_movement[code]
    elif code in key_actions:
        act = key_actions[code].key
    else:
        print("unrecognized command")
    return keydown(x, y, act)

# should change to movement process
walkChars = {
    "+": "a door",
    "o": "a lamp",
    "#": "a wall",
    "x": "a post",
    "~": "a river",
}
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
            glog.add(walkBlock.format(walkChars[ch]))
            # if ch == "+":
            #     glog.add(walkBlock.format("a door"))
            # if ch == "#":
            #     glog.add(walkBlock.format("a wall"))
                # glog.add(f"{player.x+x}, {player.y+y}")
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
    debug=False
    if debug:
        glog.add("opening inventory")
    playscreen = False

    current_range = 0
    while True:
        term.clear()
        border()
        status_box()
        log_box()
        term.puts(2, 1, "[color=white]Inventory")
        term.refresh()
        code = term.read()
        if code in (term.TK_ESCAPE, term.TK_I,):
            break
        elif code == term.TK_UP:
            if current_range > 0: current_range -= 1
        elif code == term.TK_DOWN:
            if current_range < 10: current_range += 1
    if debug:
        glog.add("Closing inventoryy")
    term.clear()
    # status_box()
    # log_box()
    # map_box()

def interactDoor(x, y, key):
    def onlyOne(container):
        return len(container) == 1

    def eightsquare(x, y):
        space = namedtuple("Space", ("x","y"))
        return [space(x+i,y+j) for i, j in list(num_movement.values())]

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
        log_box()
        map_box()
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
    'f1': dungeon._sundown,
    'f2': dungeon._sunup,
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
def graphics(integer: int) -> None:
    def toBin(n):
        return list(bin(n).replace('0b'))
    if not 0 < integer < 8:
        raise ValueError("Must be within 0-7")

def border():
    # status border
    border_line =  "[color=dark #9a8478]"+chr(toInt("25E6"))+"[/color]"
    for i in range(20):
        term.puts(SCREEN_WIDTH-20+i, 0, border_line)
        term.puts(SCREEN_WIDTH-20+i, SCREEN_HEIGHT-1, border_line)
    for j in range(35):
        term.puts(SCREEN_WIDTH-20, j, border_line)
        term.puts(SCREEN_WIDTH-1, j, border_line)
    # message log border
    for i in range(60):
        term.puts(i, SCREEN_HEIGHT-6, border_line)
        term.puts(i, SCREEN_HEIGHT-1, border_line)
    for j in range(6):
        term.puts(0, SCREEN_HEIGHT-6+j, border_line)
        #term.puts(SCREEN_WIDTH-20, SCREEN_HEIGHT-6+j,border_line)

turn = 0
def status_box():
    global player, turn
    term.puts(61, 1, f"[color=red]HP[/color]: {player.h}")
    term.puts(61, 3, f"[color=blue]MP[/color]: {player.m}")
    term.puts(61, 5, f"[color=green]SP[/color]: {player.s}")
    term.puts(61, 7, f"[color=yellow]{'day' if dungeon._sun() else 'night'}[/color]")
    term.puts(61, 9, f"[color=orange]{turn}[/color]")

def log_box():
    messages = glog.write().messages
    if messages:
        for idx in range(len(messages)):
            term.puts(1, SCREEN_HEIGHT-5+idx, messages[idx])

def map_box():
    """ Logic:
            Should first print map in gray/black
            Then print units/interactables?
            Finally light sources and player?"""
    term.composition(False)
    dungeon.fov_calc(lights+[(player.x, player.y, FOV_RADIUS)])
    for x, y, lit, ch, bkgd in list(dungeon.output(player.x, player.y, units)):
        # term.bkcolor(bgkd)
        if len(str(ch)) < 2:
            term.puts(x, y, "[color={}]{}[/color]".format(lit, ch))
        else:
            try:
                term.puts(x, y, "[color={}]".format(lit)+chr(toInt(ch))+"[/color]")
            except:
                print(lit, ch)
                raise
    term.refresh()

# End graphics functions
# ---------------------------------------------------------------------------------------------------------------------#
# Start initializations

setup()
glog = GameLogger(4)
# global game variables
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
player = Person(px, py, '@')
rat = Object(85, 30, 'r', 'white')
npc = Object(7, 7, '@', 'orange')
npc1 = Object(5, 15, '@', 'orange')
npc2 = Object(0, 56, '@', 'orange')
guard3 = Object(63, 31, '@', 'orange')
guard1 = Object(64, 32, "@", 'orange')
guard2 = Object(63, 37, "@", 'orange')
guard4 = Object(64, 37, '@', 'orange')
units = [npc, guard1, guard2, guard3, guard4, npc1, npc2, rat]
proceed = True
lr = 5
# lights = [
#     (1, 10, lr),
#     (21, 10, lr),
#     (41, 10, lr),
#     (61, 10, lr),
#     (81, 10, lr),
#     (101, 10, lr),
#     (121, 10, lr),
#     (1, 38, lr),
#     (21, 38, lr),
#     (41, 38, lr),
#     (61, 38, lr),
#     (81, 38, lr),
#     (101, 38, lr),
#     (121, 38, lr),
# ]
lights = [(121, 39, 10)]
while proceed:
    term.clear()
    status_box()
    border()
    log_box()
    map_box()
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
