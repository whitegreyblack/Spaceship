# world.py

"""World created using ecs systems and msvcrt getch for input"""

import copy
import curses
import os
import random
import time

import click

import examples.utils as utils
from classes.utils import dimensions
from ecs import (AI, Collision, Destroy, Effect, Engine, Experience, Health,
                 Information, Input, Logger, Message, Movement, Position,
                 Render, components)
from ecs.systems import systems
from keyboard import keyboard
from maps import Map, RayCastedMap, dungeons
from space import eight_square, nine_square


def curses_setup(screen):
    curses.curs_set(0)
    curses.init_pair(1, curses.COLOR_WHITE, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_WHITE, curses.COLOR_YELLOW)
    curses.init_pair(3, curses.COLOR_WHITE, curses.COLOR_RED)
    screen.border()
    screen.addstr(0, 1, '[__main__]')

def find_empty_space(engine):
    positions = engine.position.components.values()
    unit_positions = set((position.x, position.y) for position in positions)
    open_spaces = engine.world.floors.difference(unit_positions)
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
    player = engine.entities.create()
    # engine.ai.add(player, AI())
    engine.input.add(player, Input())
    space = find_empty_space(engine)
    if not space:
        raise Exception("No empty spaces to place player")
    engine.position.add(player, Position(*space))
    engine.render.add(player, Render('@'))
    engine.health.add(player, Health(20, 20))
    engine.information.add(player, Information("you"))
    engine.add_player(player)

def add_computers(engine, npcs):
    positions = engine.position.components.values()
    for _ in range(npcs):
        computer = engine.entities.create()
        space = find_empty_space(engine)
        if not space:
            break
        engine.input.add(computer, Input())
        engine.position.add(computer, Position(*space))
        engine.render.add(computer, Render('g'))
        engine.ai.add(computer, AI())
        engine.information.add(computer, Information("goblin"))
        engine.health.add(computer, Health(2, 2))

def add_items(engine):
    item = engine.entities.create()
    open_spaces = set(engine.world.spaces())
    if not open_spaces:
        return engine
    space = open_spaces.pop()
    engine.position.add(
        item, 
        Position(*space, blocks_movement=False)
    )
    engine.render.add(item, Render('%'))
    engine.information.add(item, Information("item"))
    engine.logger.add(f"{item.id} @ ({space})") # show us item position

def ecs_setup(screen, dungeon, npcs):
    engine = Engine(
        components=components, 
        systems=systems,
        # world=Map.factory(dungeon),
        world=RayCastedMap(dungeon),
        screen=screen,
        keyboard=keyboard
    )
    # print(engine)
    add_player(engine)
    add_computers(engine, npcs)
    # add_items(engine)

    engine.logger.add(f"count: {len(engine.entities.entities)}")
    return engine

def main(screen, dungeon, npcs):
    curses_setup(screen)
    dungeon = dungeons.get(dungeon.lower(), 'small')
    engine = ecs_setup(screen, dungeon=dungeon, npcs=npcs)
    engine.run()

@click.command()
@click.option('-d', '--dungeon', default='dungeon')
@click.option('-n', '--npcs', default=0)
def preload(dungeon, npcs):
    curses.wrapper(main, dungeon, npcs)

if __name__ == "__main__":
    preload()
