# componentmanager.py

"""Base class for component manager"""

# TODO: should we allow duplicate entity?

from dataclasses import dataclass
from dataclasses import field

@dataclass
class EntityComponent:
    entity: object
    component: object

class Manager(object):
    def __init__(self):
        self.components = []

    def add(self, entity, component):
        entity_component = EntityComponent(entity, component)
        self.components.append(entity_component)

    def remove(self, entity):
        self.components.remove()
        
    def find(self, entity):
        ...
