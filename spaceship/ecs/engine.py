# engine.py

"""Engine class to hold all objects"""

import time

from ecs.common import Logger, Map, render_main_menu, direction_from_input, direction_from_random
from ecs import Movement, Collision
from ecs.managers import ComponentManager, EntityManager
from ecs.systems import CollisionSystem, MovementSystem
import curses

from space import nine_square
import random

class Engine(object):
    def __init__(self, components, systems, world=None, screen=None, keyboard=None):
        self.running = True
        self.logger = Logger()
        self.debugger = Logger()
        self.entities = EntityManager()
        # self.components = {}
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
        # systems = []
        for attr in self.__dict__.keys():
            if attr.endswith('_manager'):
                managers.append(attr.replace('_manager', ''))
            # if attr.endswith('_system'):
            #     systems.append(attr)
        return f"Engine({', '.join(managers)})" #, {', '.join(systems)})"

    def init_managers(self, components):
        # self.components = {}
        for component in components:
            # self.components[component.classname()] = component
            # name = f"{component.classname()}_manager"
            # manager = ComponentManager(component)
            self.__setattr__(
                component.classname(),
                ComponentManager(component)
            )

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

    def get_manager(self, component):
        manager = getattr(self, component)
        if not manager:
            raise Exception(f"No component of type name: {component}")
        return manager

    def run(self):
        while True:
            self.render_system.process()
            self.input_system.process() # per entity turn
            self.graveyard_system.process()
            if not self.running:
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
