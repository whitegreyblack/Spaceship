# entitymanager.py

"""Manager for entity objects"""

from dataclasses import dataclass


@dataclass
class Entity:
    __slots__ = ['id']
    id: int

class EntityManager(object):
    __slots__ = ['next_id', 'ids', 'entities', 'removed']
    
    def __init__(self):
        self.next_id = 0
        self.ids = set()
        self.removed = set()
        self.entities = []

    def __repr__(self):
        return f"{self.__class__.__name__}(next_id={self.next_id})"

    def __iter__(self):
        for entity in self.entities:
            yield entity

    def create(self, entity_id=None):
        if not entity_id:
            entity_id = self.next_id
            self.next_id += 1
        entity = Entity(entity_id)
        self.ids.add(entity_id)
        self.entities.append(entity)
        return entity

    def find(self, eid):
        for e in self.entities:
            if e.id == eid:
                return e
        return None

    def remove(self, entity):
        self.ids -= {entity.id}
        # careful though. components not removed entirely can be accesed if id is reused
        self.removed.add(entity.id)
        self.entities.remove(entity)

if __name__ == "__main__":
    from ecs.util import dprint
    manager = EntityManager()
    print(dprint(manager), '# check next_id value')
    entity = manager.create()
    print(dprint(entity))
    print(dprint(manager), '# verify next_id value incremented')

    e = manager.create()
    print(e.id)
    print(manager.next_id)

    f = manager.create(e.id)
    print(f.id)
    print(manager.next_id)
