# input_system.py

"""Input system"""

import random
import time

from ecs import Movement
from space import eight_square, nine_square
import curses
from .system import System


class InputSystem(System):

    def direction_from_input(self):
        curses.flushinp()
        char = self.engine.get_input()
        # check exit input
        if char == ord('q') or char == 27:
            self.engine.running = False
            return None
        # check inventory command
        self.engine.logger.add(
            f"{char}, {repr(char)}, {chr(char)}"
        )
        command = self.engine.keyboard.get(char, None)
        if not command:
            self.engine.logger.add("Command unknown")
        return command
    
    def direction_from_random(self, entity):
        position = self.engine.position_manager.find(entity)
        possible_spaces = []
        for x, y in nine_square():
            if not 0 <= position.x + x < self.engine.world.width:
                continue
            if not 0 <= position.y + y < self.engine.world.height:
                continue
            cell = self.engine.world.array[position.y+y][position.x+x]
            if cell not in ('#', '+'):
                possible_spaces.append((x, y))
        index = random.randint(0, len(possible_spaces)-1)
        return possible_spaces[index]

    def process(self):
        entities = self.engine.entity_manager.entities
        positions = self.engine.position_manager
        ais = self.engine.ai_manager
        for entity in self.engine.entity_manager.entities:
            ai = ais.find(entity)
            position = positions.find(entity)
            if not position:
                continue
            while 1:
                if not ai:
                    x, y = self.direction_from_input()
                else:
                    x, y = self.direction_from_random(entity)
                self.engine.add_component(entity, 'movement', x, y)
                result = self.engine.movement_system.process()
                if result:
                    break
    
    def process_entity(self, entity):
        ai = self.engine.ai_manager.find(entity)
        x, y = None, None
        if ai:
            x, y = self.direction_from_random(entity)
            self.engine.movement_manager.add(entity, Movement(x, y))
            self.engine.movement_system.process_movement(entity)

        elif self.engine.player == entity:
            while 1:
                command = self.direction_from_input()
                if not self.engine.running: # can only be stopped here by user
                    return
                if not command:
                    self.engine.render_system.process()
                    continue
                self.engine.movement_manager.add(
                    entity, 
                    Movement(command[1], command[2])
                )
                result = self.engine.movement_system.process_movement(entity)
                self.engine.movement_manager.remove(entity)
                if result:
                    break
