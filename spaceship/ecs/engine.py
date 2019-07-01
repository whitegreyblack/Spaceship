# engine.py

"""Engine class to hold all objects"""

import curses
import random
import time
from dataclasses import dataclass, field

from ecs import Collision, Movement, Position, Information, Openable
from ecs.common import (Logger, Map, direction_from_input,
                        direction_from_random, render_main_menu)
from ecs.managers import ComponentManager, EntityManager
from ecs.systems import CollisionSystem, MovementSystem
from space import nine_square


@dataclass
class Result:
    events: list = field(default_factory=list)
    made_progress: bool = False
    @property
    def refresh():
        return made_progress or events

class Engine(object):
    def __init__(
            self, 
            components, 
            systems,
            # world=None, 
            terminal=None, 
            keyboard=None
    ):
        self.running = True
        self.logger = Logger()
        self.debugger = Logger()
        self.entity = 0
        self.entities = EntityManager()
        # self.components = {}
        self.init_managers(components)
        self.init_systems(systems)
        # self.init_world(world)
        self.map_x_offset = 1
        self.map_y_offset = 1
        self.add_terminal(terminal)
        self.keyboard = keyboard

    def __repr__(self):
        attributes = []
        # systems = []
        for attr, value in self.__dict__.items():
            if isinstance(value, ComponentManager):
                attributes.append(attr)
        return f"Engine({', '.join(attributes)})"

    def init_managers(self, components):
        for component in components:
            self.__setattr__(
                component.manager,
                ComponentManager(component)
            )

    def init_systems(self, systems):
        for system_type in systems:
            name = f"{system_type.classname().replace('system', '')}_system"
            system = system_type(self)
            self.__setattr__(name, system)

    def get_input(self):
        # curses.flushinp()
        return self.terminal.getch()

    def keypress_from_input(self, char):
        return self.keyboard.get(char, None)

    def find_entity(self, entity_id):
        return self.entity_manager.find(entity_id)

    def add_world(self, world):
        if hasattr(self, 'world') and getattr(self, 'world'):
            raise Exception("world already initialized")
        self.world = world

    def add_screen(self, name, screen):
        if hasattr(self, name):
            raise AttributeError(f"Attribute already set: {name}.")
        self.__setattr__(name, screen)

    def add_terminal(self, terminal):
        if not terminal:
            return
        if hasattr(self, 'terminal') and getattr(self, 'terminal'):
            raise Exception("terminal already initialized")
        self.terminal = terminal
        self.height, self.width = terminal.getmaxyx()

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
            start = time.time()
            self.render_system.render_fov()
            self.render_system.process()
            # per entity turn
            # self.turn_system.process()
            # print(time.time() - start)
            self.input_system.process()
            # self.graveyard_system.process()
            if not self.running:
                break

    # def process_command(self, command):
    #     if command == 

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
