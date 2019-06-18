# msvcrt_loop.py

"""Demo using msvcrt to get keyboard output values"""

import copy
import msvcrt
import os
import sys
import time

from classes.utils import dimensions
from ecs.component_manager import ComponentManager
from ecs.components.position import Position
from ecs.entity import Entity
from ecs.entity_manager import EntityManager

from demos.utils import LARGE_DUNGEON

TEST_MAP = """
#######
#.....#
#..#..#
#.....#
#######"""[1:]

def print_world(world, entity_manager, position_manager):
    worldcopy = copy.deepcopy(world)
    for entity_id, position in position_manager.components.items():
        worldcopy[position.y][position.x] = '@'
    print('\n'.join(''.join(row) for row in worldcopy))

def main():
    entity_manager = EntityManager()
    position_manager = ComponentManager(Position)
    entity = entity_manager.create() 
    position = Position(1, 1)   
    position_manager.add(entity, position)

    turns = 0
    world, width, height = dimensions(LARGE_DUNGEON)
    os.system('cls')
    print(turns, '@60 frames/s || .15s sleep')
    print_world(world, entity_manager, position_manager)
    while 1:
        string = None
        fnkey = None
        char = msvcrt.getch()
        if char == b'\x03' or char == b'\x1b':
            print(char)
            break
        if char == b'\xe0':
            fnkey = msvcrt.getch()
            if fnkey == b'H':
                string = 'down'
                position.y = max(0, position.y - 1)
            elif fnkey == b'P':
                string = 'up'
                position.y = min(height - 1, position.y + 1)
            elif fnkey == b'K':
                string = 'left'
                position.x = max(0, position.x - 1)
            elif fnkey == b'M':
                position.x = min(width - 1, position.x + 1)
                string = 'right'
        os.system('cls')
        print(turns, '@60 frames/s || .15s sleep')
        print_world(world, entity_manager, position_manager)
        print(char, fnkey, string)
        turns += 1
        time.sleep(.015)

if __name__ == "__main__":
    main()
