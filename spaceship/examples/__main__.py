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
from ecs import (
    AI, Collision, Effect, Engine, Experience, Health, Information, Logger,
    Map, Message, Movement, Position, Render, components)
from ecs.systems import systems
from space import eight_square, nine_square

# define colors
colors = {
    'red': None
}

keyboard = {
    curses.KEY_DOWN: ('move', 0, 1), # 258
    curses.KEY_UP: ('move', 0, -1), # 259
    curses.KEY_LEFT: ('move', -1, 0), # 260
    curses.KEY_RIGHT: ('move', 1, 0), # 261
    449: ('move', -1, -1), # fn-7
    450: ('move',  0, -1), # fn-8
    451: ('move',  1, -1), # fn-9
    452: ('move', -1,  0), # fn-4
    453: ('move',  0,  0), # fn-5
    454: ('move',  1,  0), # fn-6
    455: ('move', -1,  1), # fn-1
    456: ('move',  0,  1), # fn-2
    457: ('move',  1,  1), # fn-3
    104: ('move', -1,  0), # h
    106: ('move',  0,  1), # j
    107: ('move',  0, -1), # k
    108: ('move',  1,  0), # l
    117: ('move', -1,- 1), # u
    105: ('move',  1, -1), # i
    110: ('move', -1,  1), # n
    109: ('move',  1,  1), # m
    73: ('system', 'inventory') # I
}

def curses_setup(screen):
    curses.curs_set(0)
    screen.border()
    screen.addstr(0, 1, '[__main__]')

def ecs_setup(screen, npcs=1):
    engine = Engine(components=components, systems=systems)

    # world
    world =  Map.factory(LARGE_DUNGEON)
    engine.add_world(world)
    engine.map_y_offset = 1
    engine.map_x_offset = 1

    # other components
    engine.add_screen(screen)
    engine.add_keyboard(keyboard)
    
    """         position render info ai  health
    player       o        o      o        o
    computer     o        o      o    o   o
    item         o        o      o
    wall         o        o      
    """
    # player
    player = engine.entity_manager.create()
    # engine.ai_manager.add(player, AI())
    engine.position_manager.add(player, Position(1, 1))
    engine.render_manager.add(player, Render('@'))
    engine.health_manager.add(player, Health(100, 100))
    engine.information_manager.add(player, Information("you"))
    engine.add_player(player)

    # computer(s)
    positions = engine.position_manager.components.values()
    for _ in range(npcs):
        computer = engine.entity_manager.create()
        open_spaces = set(engine.world.spaces()).difference(set(
            (position.x, position.y)
                for position in positions
        ))
        if not open_spaces:
            break
        space = open_spaces.pop()
        engine.position_manager.add(computer, Position(*space))
        engine.render_manager.add(computer, Render('g'))
        engine.ai_manager.add(computer, AI())
        engine.information_manager.add(computer, Information("goblin"))
        engine.health_manager.add(computer, Health(2, 2))

    item = engine.entity_manager.create()
    open_spaces = set(engine.world.spaces())
    if not open_spaces:
        return engine
    space = open_spaces.pop()
    engine.position_manager.add(
        item, 
        Position(*space, blocks_movement=False)
    )
    engine.render_manager.add(item, Render('%'))
    engine.information_manager.add(item, Information("item"))
    engine.logger.add(f"{item.id} @ ({space})")
    return engine

def main(screen, npcs):
    curses_setup(screen)
    engine = ecs_setup(screen, npcs=npcs)
    engine.run()

@click.command()
@click.option('-n', '--npcs', default=2)
def preload(npcs):
    curses.wrapper(main, npcs)

if __name__ == "__main__":
    preload()
