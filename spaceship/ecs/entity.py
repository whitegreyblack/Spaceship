# entity.py

from dataclasses import dataclass

@dataclass
class Entity:
    __slots__ = ['id']
    id: int

if __name__ == "__main__":
    from ecs.util import dprint
    e1 = Entity(0)
    e2 = Entity(1)
    print(dprint(e1))
    print(dprint(e2))
