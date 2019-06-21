# engine.py

"""Engine class to hold all objects"""

import time

from ecs.common import Logger, Map
from ecs import Movement, Collision
from ecs.managers import ComponentManager, EntityManager
from ecs.systems import CollisionSystem, MovementSystem


class Engine(object):
    def __init__(self, components, systems):
        self.running = True
        self.logger = Logger()
        self.entity_manager = EntityManager()
        self.components = {}
        for component in components:
            self.components[component.classname()] = component
            name = f"{component.classname()}_manager"
            manager = ComponentManager(component)
            self.__setattr__(name, manager)
        for system_type in systems:
            name = f"{system_type.classname().replace('system', '')}_system"
            system = system_type(self)
            self.__setattr__(name, system)
    def __repr__(self):
        managers = []
        systems = []    
        for attr in self.__dict__.keys():
            if attr.endswith('_manager'):
                managers.append(attr.replace('_manager', ''))
            if attr.endswith('_system'):
                systems.append(attr)
        return f"Engine({', '.join(managers)}, {', '.join(systems)})"
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
    def add_keyboard(self, keyboard):
        self.keyboard = keyboard
    def add_component(self, entity, component, *args):
        manager = getattr(self, component + '_manager')
        if not manager:
            raise Exception(f"No component of type name: {component}")
        manager.add(entity, self.components[component](*args))
        # if hasattr(self, component + '_system'):
        #     system = getattr(self, component + '_system')
        #     system.process()
    def run(self):
        self.render_system.process()
        while self.running:
            self.update()
            for system in (self.render_system, self.graveyard_system):
                system.process()
    def update(self):
        entity_index = 0
        while entity_index < len(self.entity_manager.entities):
            entity = self.entity_manager.entities[entity_index]
            # self.logger.add(f"Processing action for {entity.id}")
            result = self.input_system.process_entity(entity)
            while not result:
                result = self.input_system.process_entity(entity)
            entity_index += 1

if __name__ == '__main__':
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
