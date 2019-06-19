# utils.py

"""Common data and functions used in demo"""

import copy
import os
import random

import colorama

from classes.utils import dimensions
from ecs import Entity
from ecs.common import Map
from ecs.components import (AI, Collision, Health, Information, Movement,
                            Position, Render)
from ecs.managers import ComponentManager, EntityManager

direction = {
    (0, -1): 'north',
    (0, 1): 'south',
    (-1, 0): 'west',
    (1, 0): 'east'
}

npcs_render_types = [
    ('b', colorama.Fore.BLACK, 'white'),
    ('g', colorama.Fore.GREEN, 'white'),
    ('r', colorama.Fore.BLUE, 'white')
]

npc_info = [
    'bat',
    'goblin',
    'rat'
]

messages = {
    "move": "You move {}",
    "blocked": "You try to move {} but there is someone in your way",
    "blocked_env": "You try to move {} but there is something in your way"
}

def render_logs(logger):
    messages = [logger.header, logger.world]
    for i, msg in enumerate(logger.messages):
        messages.append('...' if i else '>>> ' + msg.string)
        msg.lifetime -= 1
    print('\n'.join(messages))

def clean_logs(logger):
    logger.messages = list(filter(lambda x: x.lifetime > 0, logger.messages))
    return logger

def translate_move_input(getch, library, moveset):
    move = getch()
    if library == 'curses':
        if move == ord('q') or move == 27:
            os.system('cls')
            exit('Exit early')
        return moveset.get(move, (0, 0))
    else:
        if move == b'\x03' or move == b'q':
            os.system('cls')
            exit('Exit early')
        elif move == b'\xe0':
            alternate = getch()
            if alternate not in moveset[move]:
                return 0, 0
            return moveset[move][alternate]

def create_managers():
    # create a player entity with components
    managers = {
        k.classname(): ComponentManager(k)
            for k in (
                Position, 
                Render, 
                AI, 
                Health, 
                Collision, 
                Information, 
                Movement
            )
    }
    managers['entity'] = EntityManager()
    return managers

def create_movement(managers, entity, x, y):
    managers['movement'].add(entity, Movement(x, y))

def create_collision(managers, entity, collided_entity):
    managers['collision'].add(entity, Collision(collided_entity))

def create_player(managers):
    # add a player controlled entity which does not have an ai component
    entity = managers['entity'].create()
    managers['position'].add(entity, Position(3, 1))
    managers['render'].add(entity, Render())
    managers['health'].add(entity, Health(10, 10))
    managers['information'].add(entity, Information("You"))
    return entity

def create_unit(managers, world):
    npc_type_index = random.randint(0,len(npcs_render_types)-1)
    entity = managers['entity'].create()
    managers['position'].add(entity, Position(
        random.randint(1, world.width-2),
        random.randint(1, world.height-2)
    ))
    managers['render'].add(entity, Render(*npcs_render_types[npc_type_index]))
    managers['ai'].add(entity, AI())
    managers['information'].add(entity, Information(npc_info[npc_type_index]))
    managers['health'].add(entity, Health())

def setup(mapstring, npcs=2):
    world = Map(*dimensions(mapstring))
    managers = create_managers()
    player = create_player(managers)
    for _ in range(npcs):
        create_unit(managers, world)
    return player, world, managers

def render_units(managers):
    for entity in managers['entity'].entities:
        position = managers['position'].find(entity)
        render = managers['render'].find(entity)
        health = managers['health'].find(entity)
        ai = managers['ai'].find(entity)
        if position and render and health and health.cur_hp > 0:
            yield position.x, position.y, render.char
        elif position and render and not ai:
            yield position.x, position.y, render.char

def render_world(world, logger, managers):
    # used only in msvcrt version
    worldcopy = copy.deepcopy(world.array)
    for entity in managers['entity'].entities:
        position = managers['position'].find(entity)
        render = managers['render'].find(entity)
        health = managers['health'].find(entity)
        ai = managers['ai'].find(entity)
        # if non-player entity, show only when alive
        if position and render and health and health.cur_hp > 0:
            worldcopy[position.y][position.x] = render.string + colorama.Style.RESET_ALL
        # if player entity, print no matter what
        elif position and render and not ai:
            worldcopy[position.y][position.x] = render.char
    logger.world = '\n'.join(''.join(row) for row in worldcopy)

def render_header(logger, managers, health):
    logger.header = f"HP: {health.cur_hp}/{health.max_hp}"

def render(world, logger, managers, health):
    render_header(logger, managers, health)
    render_world(world, logger, managers)
    render_logs(logger)
