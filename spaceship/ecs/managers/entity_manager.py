# entitymanager.py

"""Manager for entity objects"""

from ecs.entity import Entity

class EntityManager(object):
    __slots__ = ['next_id', 'ids', 'entities']
    
    def __init__(self):
        self.next_id = 0
        self.ids = set()
        self.entities = []

    def __repr__(self):
        return f"{self.__class__.__name__}(next_id={self.next_id})"

    def create(self):
        entity_id = self.next_id
        entity = Entity(entity_id)
        self.ids.add(entity_id)
        self.entities.append(entity)
        self.next_id += 1
        return entity

    def find(self, eid):
        for e in self.entities:
            if e.id == eid:
                return e
        return None

    def remove(self, entity):
        self.ids -= {entity.id}
        self.entities.remove(entity)

if __name__ == "__main__":
    from ecs.util import dprint
    manager = EntityManager()
    print(dprint(manager))
    entity = manager.create_entity()
    print(dprint(entity))
    print(dprint(manager))
