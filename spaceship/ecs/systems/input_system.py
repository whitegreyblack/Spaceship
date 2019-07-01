# input_system.py

"""Input system"""

import curses
import random
import time
from dataclasses import dataclass, field

from ecs import Movement, Position, Collision
from space import eight_square, nine_square
from ecs.managers import join
from .system import System

@dataclass
class Command:
    char: str
    keypress: str

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

    def open_door(self, entity):
        """TODO: render log message when opening a door of multiple doors"""
        position = self.engine.positions.find(entity)        
        turn_over = False
        coordinates = []
        # get all cardinal coordinates surrounding current entity position
        for x, y in eight_square():
            coordinates.append((position.x + x, position.y + y))
        g = join(
            self.engine.openables, 
            self.engine.positions, 
            self.engine.renders
        )
        doors = {}
        # compare coordinates against entities that can be opened that have a
        # a position x, y value in the coordinates list.
        for entity_id, (openable, coordinate, render) in g:
            valid_coordinate = (coordinate.x, coordinate.y) in coordinates
            if valid_coordinate and not openable.opened:
                x = coordinate.x - position.x
                y = coordinate.y - position.y
                doors[(x, y)] = (openable, coordinate, render)
        door_to_open = None
        if not doors:
            self.engine.logger.add(f"No closed doors to open")
        elif len(doors) == 1:
            door_to_open, = doors.items()
        else:
            self.engine.logger.add(f"Which door to open?")
            self.engine.render_system.render_logs()
            char = self.engine.get_input()
            # invalid keypress
            if not 258 <= char < 262:
                self.engine.logger.add(f"You cancel opening a door due to input error")
                return turn_over
            keypress = self.engine.keyboard[char]
            movement = Movement.from_input(keypress)
            # valid direction keypress but not valid door direction
            door = doors.get((movement.x, movement.y), None)
            if not door:
                self.engine.logger.add(f"You cancel opening a door direction invalid error")
            door_to_open = ((movement.x, movement.y), door)
        if door_to_open:
            ((x, y), (openable, position, render)) = door_to_open
            openable.opened = True
            position.blocks_movement = False
            render.char = '/'
            self.engine.logger.add(f"You open the door")
            turn_over = True
        return turn_over    

    def close_door(self, entity):
        """TODO: cannot close door when unit is standing on the cell"""
        position = self.engine.positions.find(entity)
        turn_over = False
        coordinates = []
        for x, y in eight_square():
            coordinates.append((position.x + x, position.y + y))
        g = join(
            self.engine.openables, 
            self.engine.positions, 
            self.engine.renders
        )
        doors = {}
        # compare coordinates against entities that can be closed that have a
        # a position x, y value in the coordinates list.
        for entity_id, (openable, coordinate, render) in g:
            if (coordinate.x, coordinate.y) in coordinates and openable.opened:
                x = coordinate.x - position.x
                y = coordinate.y - position.y
                doors[(x, y)] = (openable, coordinate, render)
        door_to_close = None
        if not doors:
            self.engine.logger.add(f"No opened door to close")
        elif len(doors) == 1:
            door_to_close, = doors.items()
        else:
            self.engine.logger.add(f"Which door to open?")
            self.engine.render_system.render_logs()
            char = self.engine.get_input()
            # invalid keypress
            if not 258 <= char < 262:
                self.engine.logger.add(f"You cancel closing a door due to input error")
                return turn_over
            keypress = self.engine.keyboard[char]
            movement = Movement.from_input(keypress)
            # valid direction keypress but not valid door direction
            door = doors.get((movement.x, movement.y), None)
            if not door:
                self.engine.logger.add(f"You cancel closing a door direction invalid error")
            door_to_close = ((movement.x, movement.y), door)
        if door_to_close:
            ((x, y), (openable, position, render)) = door_to_close
            openable.opened = False
            position.blocks_movement = True
            render.char = '+'
            self.engine.logger.add(f"You close the door")
            turn_over = True
        return turn_over

    def collide(self, entity, collision):
        other = self.engine.entities.find(collision.entity_id)
        info = self.engine.infos.find(other)
        self.engine.logger.add(f'collided with a {info.name}({collision.entity_id})')

    def move(self, entity, movement) -> bool:
        position = self.engine.positions.find(entity)
        if not position or not movement:
            return False
        x, y = position.x + movement.x, position.y + movement.y
        for other_id, other_position in self.engine.positions:
            if other_id == entity.id or not other_position.blocks_movement:
                continue
            future_position_blocked = (
                (x, y) == (other_position.x, other_position.y)
            )
            if future_position_blocked:
                self.collide(entity, Collision(other_id))
                return True
        position.x += movement.x
        position.y += movement.y
        return True

    def pick_item(self, entity):
        position = self.engine.positions.find(entity)
        inventory = self.engine.inventories.find(entity)
        g = join(
            self.engine.items,
            self.engine.positions,
            self.engine.infos
        )
        descriptions = []
        items_picked_up = []
        for eid, (item, item_position, info) in g:
            if (position.x, position.y) == (item_position.x, item_position.y):
                items_picked_up.append(eid)
                descriptions.append(info.name)
        if not items_picked_up:
            return False
        for eid in items_picked_up:
            # remove from map
            entity = self.engine.entities.find(eid)
            self.engine.visibilities.remove(entity)
            self.engine.renders.remove(entity)
            self.engine.positions.remove(entity)
            # add to inventory
            inventory.items.append(entity.id)
        self.engine.logger.add(f"Picked up {', '.join(descriptions)}")
        return True

    def player_command(self, entity):
        while True:
            # self.engine.logger.add(f"Turn for {entity.id}")
            exit_prog = False
            turn_over = False
            char = self.engine.get_input()
            # print(char)
            if char == -1:
                break
            keypress = self.engine.keypress_from_input(char)
            if keypress == 'q':
                self.engine.running = False
                break
            elif keypress in ('up', 'down', 'left', 'right'):
                movement = Movement.from_input(keypress)
                # self.engine.movements.add(entity, movement)
                turn_over = self.move(entity, movement)
            elif keypress == 'escape':
                while True:
                    self.engine.render_system.main_menu.render()
                    keep_open = self.engine.render_system.main_menu.get_input()
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
                turn_over = self.open_door(entity)
            elif keypress == 'c':
                turn_over = self.close_door(entity)
            elif keypress == 'comma':
                turn_over = self.pick_item(entity)
            else:
                self.engine.logger.add(f"unknown command {char} {chr(char)}")
            if turn_over:
                break
            self.engine.render_system.process()

    def computer_command(self, entity):
        """Computer commands currently only support mindless movement"""
        position = self.engine.positions.find(entity)
        possible_spaces = []
        for x, y in nine_square():
            possible_spaces.append((x, y))
        index = random.randint(0, len(possible_spaces)-1)
        movement = Movement(*possible_spaces[index])
        return self.move(entity, movement)

    def process(self):
        for entity_id, need_input in self.engine.inputs:
            entity = self.engine.entities.find(entity_id)
            ai = self.engine.ais.find(entity)
            if ai:
                command = self.computer_command(entity)
            else:
                command = self.player_command(entity)
