# entitymanager.py

"""Manager for entity objects"""

from ecs.entity import Entity

class EntityManager(object):
    __slots__ = ['next_id', 'entities']
    
    def __init__(self):
        self.next_id = 0
        self.entities = []

    def __repr__(self):
        return f"{self.__class__.__name__}(next_id={self.next_id})"

    def create_entity(self):
        entity_id = self.next_id
        entity = Entity(entity_id)
        self.entities.append(entity)
        self.next_id += 1
        return entity

if __name__ == "__main__":
    from ecs.util import dprint
    manager = EntityManager()
    print(dprint(manager))
    entity = manager.create_entity()
    print(dprint(entity))
    print(dprint(manager))
