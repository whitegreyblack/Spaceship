# world.py

"""World created using ecs systems and msvcrt getch for input"""

import copy
import curses
import os
import random
import time

import click

import examples.utils as utils
from classes.map import LARGE_DUNGEON, LONG_DUNGEON, SMALL_DUNGEON
from classes.utils import dimensions
from ecs import Engine, Logger, Map, Message
from ecs.components import AI, Position, Render, components
from ecs.systems import systems
from space import eight_square, nine_square

keyboard = {
    curses.KEY_DOWN: (0, 1), # 258
    curses.KEY_UP: (0, -1), # 259
    curses.KEY_LEFT: (-1, 0), # 260
    curses.KEY_RIGHT: (1, 0), # 261
}

def curses_setup(screen):
    curses.curs_set(0)
    screen.border()
    screen.addstr(0, 1, '[__main__]')

def ecs_setup(screen):
    engine = Engine(components=components, systems=systems)

    world =  Map.factory(SMALL_DUNGEON)
    engine.add_world(world)
    engine.map_y_offset = 1
    engine.map_x_offset = 1

    # other components
    engine.add_screen(screen)
    engine.add_keyboard(keyboard)
    
    # player
    entity = engine.entity_manager.create()
    engine.position_manager.add(entity, Position(1, 1))
    engine.render_manager.add(entity, Render('@'))
    # engine.ai_manager.add(entity, AI())
    engine.add_player(entity)

    # computer
    entity = engine.entity_manager.create()
    engine.position_manager.add(entity, Position(4, 1))
    engine.render_manager.add(entity, Render('g'))
    engine.ai_manager.add(entity, AI())
    return engine

def main(screen):
    curses_setup(screen)
    engine = ecs_setup(screen)
    engine.run()

if __name__ == "__main__":
    curses.wrapper(main)
