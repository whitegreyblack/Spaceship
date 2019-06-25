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
        if char == ord('q'):
            self.engine.running = False
            return None, None, None
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
        for entity_id in self.engine.input.components.keys():
            entity = self.engine.entities.find(entity_id)
            position = self.engine.position.find(entity)
            ai = self.engine.ai.find(entity)
            # process player input
            if not ai:
                while True:
                    self.engine.logger.add(f"Turn for {entity.id}")
                    exit_prog = False
                    turn_over = False
                    char = self.engine.get_input()
                    keypress = self.engine.keyboard[char]
                    self.engine.logger.add(keypress)
                    if keypress == 'q':
                        self.engine.running = False
                        break
                    elif keypress in ('up', 'down', 'left', 'right'):
                        directions = {
                            258: ( 0,  1),
                            259: ( 0, -1),
                            260: (-1,  0),
                            261: ( 1,  0),
                        }
                        self.engine.movement_system.process((
                            entity, 
                            position, 
                            directions[char]
                        ))
                        turn_over = True
                    elif keypress == 'escape':
                        while True:
                            self.engine.render_system.main_menu.render()
                            keep_open = self.engine.render_system.main_menu.get_input()
                            print(keep_open, exit_prog)
                            if not self.engine.running:
                                return
                            if not keep_open:
                                break
                    elif keypress == 'i':
                        while True:
                            self.engine.render_system.inventory_menu.render()
                            keep_open = self.engine.render_system.inventory_menu.get_input()
                            if not keep_open:
                                break
                    elif keypress == 'o':
                        doors = []
                        for x, y in eight_square():
                            is_blocked = self.engine.world.is_blocked(position.x + x, position.y + y)
                            is_door = self.engine.world.is_door(position.x + x, position.y + y)
                            if is_blocked and is_door:
                                doors.append((x, y))
                        if not doors:
                            self.engine.logger.add(f"No door to open")
                        elif len(doors) == 1:
                            door = doors.pop()
                            opened = self.engine.world.open_door(position.x + door[0], position.y + door[1])
                            if opened:
                                self.engine.logger.add(f"You open the door")
                            else:
                                self.engine.logger.add(f"You cannot open the door")
                        else:
                            char = self.engine.get_input()
                            directions = {
                                258: ( 0,  1),
                                259: ( 0, -1),
                                260: (-1,  0),
                                261: ( 1,  0),
                            }
                            direction = directions.get(char, None)
                            if not direction or direction not in doors:
                                self.engine.logger.add(f"You cancel opening a door")
                            else:
                                self.engine.world.add(f"You open the door")
                                turn_over = True
                    else:
                        self.engine.logger.add(f"unknown command {char} {chr(char)}")
                    if turn_over:
                        break
                    self.engine.render_system.process()

        # entities = self.engine.entity_manager.entities
        # positions = self.engine.position_manager
        # ais = self.engine.ai_manager
        # for entity in self.engine.entity_manager.entities:
        #     ai = ais.find(entity)
        #     position = positions.find(entity)
        #     if not position:
        #         continue
        #     while 1:
        #         if not ai:
        #             x, y = self.direction_from_input()
        #         else:
        #             x, y = self.direction_from_random(entity)
        #         self.engine.add_component(entity, 'movement', x, y)
        #         result = self.engine.movement_system.process()
        #         if result:
        #             break

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
