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
from ecs import (AI, Collision, Destroy, Effect, Engine, Experience, Health,
                 Information, Input, Logger, Map, Message, Movement, Position,
                 Render, components)
from ecs.systems import systems
from space import eight_square, nine_square

# define colors
colors = {
    'red': None
}

dungeons = {
    'small': SMALL_DUNGEON,
    'long': LONG_DUNGEON,
    'large': LARGE_DUNGEON
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
    73: ('inventory', None, None), # I,
    27: ('main_menu', None, None), # ESCAPE
}

def curses_setup(screen):
    curses.curs_set(0)
    curses.init_pair(1, curses.COLOR_WHITE, curses.COLOR_RED)
    screen.border()
    screen.addstr(0, 1, '[__main__]')

def find_empty_space(engine):
    positions = engine.position_manager.components.values()
    unit_positions = set((position.x, position.y) for position in positions)
    open_spaces = set(engine.world.spaces()).difference(unit_positions)
    if not open_spaces:
        return None
    return open_spaces.pop()

"""
component-entity graph
            position render info ai  health
player       o        o      o        o
computer     o        o      o    o   o
item         o        o      o
wall         o        o      
"""
def add_player(engine):
    player = engine.entity_manager.create()
    # engine.ai_manager.add(player, AI())
    engine.input_manager.add(player, Input())
    space = find_empty_space(engine)
    if not space:
        raise Exception("No empty spaces to place player")
    engine.position_manager.add(player, Position(*space))
    engine.render_manager.add(player, Render('@'))
    engine.health_manager.add(player, Health(20, 20))
    engine.information_manager.add(player, Information("you"))
    engine.add_player(player)

def add_computers(engine, npcs):
    positions = engine.position_manager.components.values()
    for _ in range(npcs):
        computer = engine.entity_manager.create()
        space = find_empty_space(engine)
        if not space:
            break
        engine.input_manager.add(computer, Input())
        engine.position_manager.add(computer, Position(*space))
        engine.render_manager.add(computer, Render('g'))
        engine.ai_manager.add(computer, AI())
        engine.information_manager.add(computer, Information("goblin"))
        engine.health_manager.add(computer, Health(2, 2))

def add_items(engine):
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
    engine.logger.add(f"{item.id} @ ({space})") # show us item position

def ecs_setup(screen, dungeon, npcs):
    engine = Engine(
        components=components, 
        systems=systems,
        world=Map.factory(dungeon),
        screen=screen,
        keyboard=keyboard
    )
    print(engine)
    add_player(engine)
    add_computers(engine, npcs)
    # add_items(engine)

    engine.logger.add(f"count: {len(engine.entity_manager.entities)}")
    return engine

def main(screen, dungeon, npcs):
    curses_setup(screen)
    dungeon = dungeons.get(dungeon, 'small')
    engine = ecs_setup(screen, dungeon=dungeon, npcs=npcs)
    engine.run()

@click.command()
@click.option('-d', '--dungeon', default='small')
@click.option('-n', '--npcs', default=0)
def preload(dungeon, npcs):
    curses.wrapper(main, dungeon, npcs)

if __name__ == "__main__":
    preload()
