# input_system.py

"""Input system"""

import curses
import random
import time
from dataclasses import dataclass, field

from ecs import Movement, Position
from space import eight_square, nine_square

from .system import System


@dataclass
class DoorAction:
    position: object
    direction: object
    def __iter__(self):
        yield self.x
        yield self.y
    @property
    def x(self):
        return self.position.x + self.direction.x
    @property
    def y(self):
        return self.position.y + self.direction.y

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

    def open_door(self, position):
        turn_over = False
        doors = []
        for x, y in eight_square():
            target = DoorAction(position, Movement(x, y))
            is_blocked = self.engine.world.is_blocked(target.x, target.y)
            is_door = self.engine.world.is_door(target.x, target.y)
            if is_blocked and is_door:
                doors.append(target)
        if not doors:
            self.engine.logger.add(f"No closed doors to open")
        elif len(doors) == 1:
            door = doors.pop()
            opened = self.engine.world.open_door(door.x, door.y)
            if opened:
                self.engine.logger.add(f"You open the door")
            else:
                self.engine.logger.add(f"You cannot open the door")
        else:
            char = self.engine.get_input()
            directions = {
                258: Movement( 0,  1),
                259: Movement( 0, -1),
                260: Movement(-1,  0),
                261: Movement( 1,  0),
            }
            direction = directions.get(char, None)
            if not direction or direction not in doors:
                self.engine.logger.add(f"You cancel opening a door")
            else:
                self.engine.world.add(f"You open the door")
                turn_over = True
        return turn_over

    def close_door(self, position):
        turn_over = False
        doors = []
        for x, y in eight_square():
            target = DoorAction(position, Movement(x, y))
            is_unblocked = not self.engine.world.is_blocked(*target)
            is_door = self.engine.world.is_door(*target)
            if is_door and is_unblocked:
                doors.append(target)
        if not doors:
            self.engine.logger.add(f"No opened door to close")
        elif len(doors) == 1:
            door = doors.pop()
            closed = self.engine.world.close_door(*door)
            if closed:
                self.engine.logger.add(f"You close the door")
            else:
                self.engine.logger.add(f"You cannot close the door")
                turn_over = True
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
                        turn_over = self.open_door(position)
                    elif keypress == 'c':
                        turn_over = self.close_door(position)
                    else:
                        self.engine.logger.add(f"unknown command {char} {chr(char)}")
                    if turn_over:
                        break
                    self.engine.render_system.process()

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
