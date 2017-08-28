# main implementation of core mechanics
from tools import bresenhams, movement, deltanorm, lambdafunc
from movement import key_movement, num_movement
from objects import Object, Tile, Map
from bearlibterminal import terminal as term
from ctypes import c_uint32, addressof
from namedlist import namedlist
from maps import MAPS
from time import time, sleep
from random import randint

# global terminal variables
SCREEN_WIDTH, SCREEN_HEIGHT = 80, 24
# LIMIT_FPS = 30 -- later used in sprite implementation
blocked = []

# ---------------------------------------------------------------------------------------------------------------------#
# TERMINAL SETUP & IMAGE IMPORTS
def setup():
    term.open()
    term.set("window: size={}x{}, title='Main Game'".format(SCREEN_WIDTH, SCREEN_HEIGHT))
# ---------------------------------------------------------------------------------------------------------------------#

# ---------------------------------------------------------------------------------------------------------------------#
# Keyboard input

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
        term.puts(x, y, ('[color={}]'+i+'[/color]').format(c))

# End graphics functions
# ---------------------------------------------------------------------------------------------------------------------#


# ---------------------------------------------------------------------------------------------------------------------#
# Start initializations
setup()
# global game variables
FOV_RADIUS = 10
MAP_WIDTH, MAP_HEIGHT = 24, 48
MAP_FACTOR = 2
COLOR_DARK_WALL = term.color_from_argb(128, 0, 0, 100)
COLOR_DARK_GROUND = term.color_from_argb(128, 50, 50, 150)
#px, py = SCREEN_WIDTH//2, SCREEN_HEIGHT//2
px, py = 5, 5
dungeon = Map(MAPS.DUNGEON)
player = Object(px, py, '@')
npc = Object(px-3, py-2, '@', 'orange')
units = [player, npc]
proceed = True

while proceed:
    term.clear()
    dungeon.fov_calc(player.x, player.y, FOV_RADIUS)
    positions = [(x, y, lit, ch) for x, y, lit, ch in dungeon.output(player.x, player.y)]
    for x, y, lit, ch in positions:
        term.puts(x, y, "[color={}]{}[/color]".format(lit, ch))
    term.refresh()
    key_in()
# End Initiailiation
# ---------------------------------------------------------------------------------------------------------------------#
