# engine.py

"""Engine class to hold all objects"""

import time

from ecs.common import Logger, Map
from ecs import Movement, Collision
from ecs.managers import ComponentManager, EntityManager
from ecs.systems import CollisionSystem, MovementSystem
import curses

from space import nine_square
import random

def render_main_menu(engine):
    engine.screen.clear()
    engine.screen.border()

    index = 0
    options = ['back', 'save', 'quit']

    # title
    engine.screen.addstr(0, 1, '[main_menu]')
    
    x = engine.width // 2
    y = engine.height // 2
    
    option_y_offset = - 1
    option_x_offset = - (max(map(len, options)) // 2)
    current_x_offset = -2

    while True:
        engine.screen.clear()
        for i, option in enumerate(options):
            engine.screen.addstr(
                y + option_y_offset + i,
                x + option_x_offset + (current_x_offset if i == index else 0),
                f"{'> ' if i == index else ''}{option}"
            )
        engine.screen.refresh()
        char = engine.screen.getch()
        if char == ord('q') or (char == 10 and options[index] == 'quit'):
            engine.running = False
            curses.endwin()
            break
        elif char == 27:
            break
        elif char == 258:
            index = (index + 1) % len(options)
        elif char == 259:
            index = (index - 1) % len(options)
    return True

def direction_from_input(engine):
    curses.flushinp()
    char = engine.get_input()
    # check exit input
    if char == ord('q'):
        engine.running = False
        return None, None, None
    # check inventory command
    engine.logger.add(
        f"{char}, {repr(char)}, {chr(char)}"
    )
    print(f"{char}, {repr(char)}, {chr(char)}")
    command = engine.keyboard.get(char, None)
    if not command:
        engine.logger.add("Command unknown")
    return command

def direction_from_random(engine, entity):
    position = engine.position_manager.find(entity)
    possible_spaces = []
    for x, y in nine_square():
        if not 0 <= position.x + x < engine.world.width:
            continue
        if not 0 <= position.y + y < engine.world.height:
            continue
        cell = engine.world.array[position.y+y][position.x+x]
        if cell not in ('#', '+'):
            possible_spaces.append((x, y))
    index = random.randint(0, len(possible_spaces)-1)
    return possible_spaces[index]

class Engine(object):
    def __init__(self, components, systems, world=None, screen=None, keyboard=None):
        self.running = True
        self.logger = Logger()
        self.debugger = Logger()
        self.entity_manager = EntityManager()
        self.components = {}
        self.init_managers(components)
        self.init_systems(systems)
        self.world = world
        self.map_x_offset = 1
        self.map_y_offset = 1
        if screen:
            self.add_screen(screen)
        if keyboard:
            self.keyboard = keyboard

    def __repr__(self):
        managers = []
        systems = []
        for attr in self.__dict__.keys():
            if attr.endswith('_manager'):
                managers.append(attr.replace('_manager', ''))
            if attr.endswith('_system'):
                systems.append(attr)
        return f"Engine({', '.join(managers)}, {', '.join(systems)})"

    def init_managers(self, components):
        self.components = {}
        for component in components:
            self.components[component.classname()] = component
            name = f"{component.classname()}_manager"
            manager = ComponentManager(component)
            self.__setattr__(name, manager)

    def init_systems(self, systems):
        for system_type in systems:
            name = f"{system_type.classname().replace('system', '')}_system"
            system = system_type(self)
            self.__setattr__(name, system)

    def get_input(self):
        return self.screen.getch()

    def find_entity(self, entity_id):
        return self.entity_manager.find(entity_id)

    def add_world(self, world):
        if hasattr(self, 'world') and getattr(self, 'world'):
            raise Exception("world already initialized")
        self.world = world

    def add_screen(self, screen):
        if hasattr(self, 'screen') and getattr(self, 'screen'):
            raise Exception("screen already initialized")
        self.screen = screen
        self.height, self.width = screen.getmaxyx()

    def add_player(self, entity):
        self.player = entity
        self.player_id = entity.id

    def add_component(self, entity, component, *args):
        manager = getattr(self, component + '_manager')
        if not manager:
            raise Exception(f"No component of type name: {component}")
        manager.add(entity, self.components[component](*args))

    # def run(self):
    #     self.render_system.process()
    #     while self.running:
    #         self.update()
    #         for system in (self.render_system, self.graveyard_system):
    #             system.process()

    # def update(self):
    #     entity_index = 0
    #     while entity_index < len(self.entity_manager.entities):
    #         if not self.running:
    #             break
    #         entity = self.entity_manager.entities[entity_index]
    #         # self.logger.add(f"Processing action for {entity.id}")
    #         self.input_system.process_entity(entity)
    #         entity_index += 1

    def run(self):
        while True:
            self.render_system.process()
            self.update()
            self.graveyard_system.process()
            if not self.running:
                break
        # while self.running:
        #     self.update()
        #     for system in (self.render_system, self.graveyard_system):
        #         system.process()
        # self.get_input()
        self.render_system.process()
        # print('get input()')

    def update(self):
        entity_index = 0
        while entity_index < len(self.entity_manager.entities):
            entity = self.entity_manager.entities[entity_index]
            # self.logger.add(f"Processing action for {entity.id}")
            while True:
                finished = self.process(entity)
                if finished:
                    break
            if not self.running:
                break
            entity_index += 1

    def process(self, entity):
        finished = True
        if not self.input_manager.find(entity):
            return finished
        ai = self.ai_manager.find(entity)
        action = 'move'
        if ai:
            x, y = direction_from_random(self, entity)
        else:
            action, x, y = direction_from_input(self)
        print(action, x, y)
        if not any((action, x, y)):
            self.running = False
        if action == 'move':
            position = self.position_manager.find(entity)
            movement = Movement(x, y)
            print(position, movement)
            x, y = position.x + movement.x, position.y + movement.y

            space_blocked = False
            if self.world.blocked(x, y):
                self.collision_manager.add(entity, Collision(x=x, y=y))
                space_blocked = True

            if not space_blocked:            
                for other_id, other_position in self.position_manager.components.items():
                    if other_id == entity.id:
                        continue
                    space_blocked = (
                        (x, y) == (other_position.x, other_position.y)
                    )
                    if space_blocked:
                        self.collision_manager.add(entity, Collision(other_id))
                        break

            position.x, position.y = x, y
            return finished
        elif action == 'main_menu':
            while True:
                menu_open = render_main_menu(self)
                self.render_system.process()
                if menu_open:
                    break

if __name__ == '__main__':
    from ecs import Position, Information
    from ecs.util import dprint
    e = Engine(
        components=(
            Position,
            Information
        ),
        systems=(
            MovementSystem,
            CollisionSystem
        )
    )
    print(dprint(e))
