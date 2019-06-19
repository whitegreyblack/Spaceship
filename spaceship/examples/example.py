# world.py

"""World created using ecs systems and msvcrt getch for input"""

import copy
import os
import random
import time

import click

import demos.utils as utils
from classes.utils import dimensions
from ecs.common import Logger, Message
from space import eight_square, nine_square

map_y_offset = 1
map_x_offset = 0

library = None
moveset = None

""" -- heuristic pathfinding
player = em.find_entity(0)
position = pm.find(player)

for e in em.entities:
    ai = am.find(e)
    pos = pm.find(e)
    if not pos and not ai:
        continue
    if pos and not ai:
        x, y = utils.translate_move_input(getch, library)
    elif pos and ai:
        possible_spaces = []
        for x, y in nine_square():
            # calculate distances to player
            d = distance(pos.x+x, pos.y+y, position.x, position.y)
            if world[pos.y+y][pos.x+x] not in ('#', '+'):
                possible_spaces.append((x, y, d))
        index = randint(0, len(possible_spaces)-1)
        possible_spaces.sort(key=lambda x: x[2])
        x, y, _ = possible_spaces[0]
"""

def input_system(world, logger, move, managers):
    for entity in managers['entity'].entities:
        entity_ai = managers['ai'].find(entity)
        entity_position = managers['position'].find(entity)

        # necessary components not found or unmovable
        if not entity_position or not entity_position.moveable:
            continue

        # get x, y for either player or computer
        if not entity_ai:
            x, y = utils.translate_move_input(move, library, moveset)
        elif entity_ai:
            possible_spaces = []
            for x, y in nine_square():
                cell = world[entity_position.y+y][entity_position.x+x] 
                if cell not in ('#', '+'):
                    possible_spaces.append((x, y))
            index = random.randint(0, len(possible_spaces)-1)
            x, y = possible_spaces[index]
        utils.create_movement(managers, entity, x, y)

def move_system(world, logger, managers):
    for entity_id, entity_movement in managers['movement'].components.items():
        entity = managers['entity'].find(entity_id)
        entity_position = managers['position'].find(entity)
        entity_ai = managers['ai'].find(entity)
        x = entity_position.x + entity_movement.x
        y = entity_position.y + entity_movement.y

        # check environment
        if world[y][x] in ('#', '+'):
            if not entity_ai:
                direction = utils.direction[(entity_movement.x, entity_movement.y)]
                message = utils.messages['blocked_env'].format(direction)
                logger.messages.append(Message(message, 1))
            continue

        # check other units
        unit_blocked = False
        for other_entity_id, other_position in managers['position'].components.items():
            if other_entity_id == entity.id:
                continue
            # NOTE: should be using the future positions of other units. 
            #     : Maybe create a local position manager to compare future position to?
            future_position_blocked = (
                (x, y) == (other_position.x, other_position.y)
            )
            if future_position_blocked:
                utils.create_collision(managers, entity, other_entity_id)
                # if not entity_ai:
                #     x, y = entity_movement.x, entity_movement.y
                #     direction = utils.direction[(x, y)]
                #     message = utils.messages['blocked'].format(direction)
                #     logger.messages.append(Message(message, 1))
                unit_blocked = True
                break
        
        # all checks pass -- move position
        if not unit_blocked:
            entity_position.x += entity_movement.x
            entity_position.y += entity_movement.y
            # if not entity_ai:
            #     direction = utils.direction[(entity_movement.x, entity_movement.y)]
            #     message = utils.messages['move'].format(direction)
            #     logger.messages.append(Message(message, 1))

def collision_system(logger, managers):
    for entity_id, collision in managers['collision'].components.items():
        collider = managers['entity'].find(entity_id)
        collider_ai = managers['ai'].find(collider)    
        collider_info = managers['information'].find(collider)
        collider_health = managers['health'].find(collider)
        if collider_health.cur_hp < 1:
            continue

        collidee_entity = managers['entity'].find(collision.collided_entity_id)
        collidee_info = managers['information'].find(collidee_entity)
        collidee_health = managers['health'].find(collidee_entity)
        if collidee_health.cur_hp < 1:
            continue

        collidee_hitpoints = collidee_health.cur_hp
        collidee_health.cur_hp -= 1
        ai = False
        if collider_ai:
            ai = True
        logger.messages.append(
            Message(
                f"{collider_info.name.capitalize()} hit{'s' if ai else ' the'} {collidee_info.name} for 1 damage",
                1
            )
        )
    managers['collision'].components.clear()

def graveyard_system(logger, managers):
    entities_to_remove = []
    for entity_id, health in managers['health'].components.items():
        entity = managers['entity'].find(entity_id)
        info = managers['information'].find(entity)
        if health.cur_hp < 1:
            entities_to_remove.append(entity)
            ai = managers['ai'].find(entity)
    for entity in entities_to_remove:
        for manager in managers.values():
            manager.remove(entity)
    
def main_msvcrt(msvcrt):
    getch = msvcrt.getch
    logger = Logger()
    mapstring = utils.LARGE_DUNGEON
    player, world, managers = utils.setup(mapstring, 10)
    player_health = managers['health'].find(player)

    # uses msvcrt getch() command
    os.system('cls')
    utils.render(world, logger, managers, player_health)
    logger = utils.clean_logs(logger)

    while managers['entity'].find(player.id):
        input_system(world.array, logger, getch, managers)
        move_system(world.array, logger, managers)
        # os.system('cls')
        # utils.render(world, logger, managers, player_health)
        collision_system(logger, managers)
        
        # utils.render_header(logger, player_health)
        # utils.render_world(world, logger, managers)
        os.system('cls')
        utils.render(world, logger, managers, player_health)
        
        graveyard_system(logger, managers)
        
        # utils.render_header(logger, player_health)
        
        # utils.render_header(logger, player_health)
        # utils.render_world(world, logger, managers)
        # utils.render_logs(logger)
        logger = utils.clean_logs(logger)
        time.sleep(.015) # helps with refresh flashes

def main_curses(screen, curses):
    getch = screen.getch
    logger = Logger()
    mapstring = utils.LARGE_DUNGEON
    player, world, managers = utils.setup(mapstring, npcs=1)
    player_health = managers['health'].find(player)

    curses.curs_set(0) # turn of curses blinking

    # do while
    screen.clear()
    utils.render_header(logger, managers, player_health)
    screen.addstr(0, 0, logger.header)
    screen.addstr(map_y_offset, map_x_offset, mapstring)
    units = utils.render_units(managers)
    for x, y, c in units:
        screen.addch(y + map_y_offset, x + map_x_offset, c)
    screen.refresh()

    while player.id in managers['entity'].ids:
        move_system(world.array, logger, getch, managers)
        screen.clear()
        collision_system(logger, managers)
        utils.render_header(logger, player_health)
        screen.addstr(0, 0, logger.header)
        graveyard_system(logger, managers)
        screen.addstr(map_y_offset, map_x_offset, mapstring)
        for x, y, c in utils.render_units(managers):
            screen.addch(y + map_y_offset, x + map_x_offset, c)
        for y, message in enumerate(logger.messages):
            message.lifetime -= 1
            screen.addstr(world.height + map_y_offset + y, 0, message.string)
        screen.refresh()
        utils.clean_logs(logger)

@click.command()
@click.option('-c', '--curses', 'curses', is_flag=True, default=False)
def preload(curses):
    global moveset, library
    if curses:
        from demos.util_curses import curses, moveset as curses_moveset
        library = 'curses'
        moveset = curses_moveset
        curses.wrapper(main_curses, curses)
    else:
        from demos.util_msvcrt import msvcrt, moveset as msvcrt_moveset
        import colorama
        colorama.init()
        library = 'msvcrt'
        moveset = msvcrt_moveset
        main_msvcrt(msvcrt)

if __name__ == "__main__":
    preload()
