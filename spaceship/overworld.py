# Overworld.py
# rewrite of new_game to refactor out unused code
from bearlibterminal import terminal as term
from collections import namedtuple
from random import choice, randint
from PIL import Image, ImageDraw
from namedlist import namedlist
from time import clock
from sys import path as syspath
from os import path as ospath
syspath.insert(0, ospath.dirname(ospath.abspath(__file__))+'/../')

# from spaceship.action import (action, key_actions, key_movement, keypress,
#                               num_movement)
# from spaceship.constants import GAME_SCREEN_HEIGHT as SCREEN_HEIGHT
# from spaceship.constants import GAME_SCREEN_WIDTH as SCREEN_WIDTH
# from spaceship.constants import FOV_RADIUS
# from spaceship.create_character import create_character as create
# from spaceship.gamelog import GameLogger
# from spaceship.manager import UnitManager
# from spaceship.maps import hexone, hextup, stringify, toInt
# from spaceship.objects import Character, Item, Map, Object, Player
# from spaceship.screen_functions import center
# from spaceship.setup import output, palette, setup, setup_font, setup_game
# from spaceship.tools import bresenhams, deltanorm, movement

OVERWORLD_PATH = "../assets/worldmap.png"

# stringify_map()
# stringify_world()
# def stringify(string, debug=False):
#     """Takes in a file location string and a bool for debug
#     to determine output. Sister function to asciify. Uses 
#     only keyboard accessible characters in the map."""

#     lines = []
#     colors = set()

#     with Image.open(string) as img:
#         pixels = img.load()
#         w, h = img.size

#     for j in range(h):
#         line = ""
#         for i in range(w):
#             # sometimes alpha channel is included so test for all values first
#             try:
#                 r, g, b, _ = pixels[i, j]
#             except ValueError:
#                 r, g, b = pixels[i, j]
#             if (r, g, b) not in colors:
#                 colors.add((r, g, b))
#             try:
#                 line += stringify_chars[(r, g, b)]
#             except KeyError:
#                 print((r, g, b))
#         lines.append(line)

#     if debug:
#         print("\n".join(lines))
#         print(colors)

#     return "\n".join(lines)
class Map:
    def __init__(self, path):
        self.world = Map.stringify_world(path)

    @staticmethod
    def stringify_world(path):
        # double for loop and build
        lines = []
        colors = set()
        with Image.open(path) as img:
            pixels = img.load()
            w, h = img.size

        for j in range(h):
            line = ""
            for i in range(w):
                try:
                    r, g, b, _ = pixels[i, j]
                except ValueError:
                    r, g, b = pixels[i, j]
                if (r, g, b) not in colors:
                    colors.add((r, g, b))
                try:
                    line += map_keys[(r, g, b)]
                except KeyError:
                    print((r, g, b))
            lines.append(list(line))
        return lines

    def draw(self):
        term.clear()
        for i in range(self.world):
            for j in range(self.world[i]):
                term.puts(j, i, self.world[i][j])
        term.refresh()
        term.read()

    def draw_dungeon(self, x=None, y=None, l=0):
        pass


def overworld(character=None):
    world = Map(OVERWORLD_PATH) 
    world.draw()

if __name__ == "__main__":
    overworld()