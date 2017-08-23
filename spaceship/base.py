# main implementation of core mechanics
from tools import bresenhams, movement, deltanorm, lambdafunc
from objects import Object
from bearlibterminal import terminal as term
from ctypes import c_uint32, addressof
from namedlist import namedlist
from time import time, sleep
from random import randint

# global terminal variables
SCREEN_WIDTH, SCREEN_HEIGHT = 80, 24
MAP_WIDTH, MAP_HEIGHT = 24, 48
MAP_FACTOR = 2
# LIMIT_FPS = 30 -- later used in sprite implementation

# global game variables
px, py = SCREEN_WIDTH//2, SCREEN_HEIGHT//2
player = Object(px, py, '@')
npc = Object(px-3, py-2, '@', 'orange')
units = [player, npc]
proceed = True

# key/value codes for movement
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

def key_in():
    global player, proceed

    # movement
    code = term.read()
    if code in (term.TK_ESCAPE, term.TK_CLOSE):
        proceed=False
    
    x, y = 0, 0
    if code in key_movement:
        x, y = key_movement[code]
    elif code in num_movement:
        x, y = num_movement[code]

    player.move(x, y)

def setup():
    term.open()
    term.set("window: size={}x{}, title='Main Game'".format(SCREEN_WIDTH, SCREEN_HEIGHT))

# ---------------------------------------------------------------------------------------------------------------------#
# Start initializations here
setup()

while proceed:
    term.clear()
    for unit in units:
        x, y, i, c = unit.draw()
        term.puts(x, y, ('[color={}]'+i+'[/color]').format(c))
    term.refresh()
    key_in()
