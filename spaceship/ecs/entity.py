# entity.py

from dataclasses import dataclass
from util import dprint, size

@dataclass
class Entity:
    __slots__ = ['id']
    id: int

if __name__ == "__main__":
    e1 = Entity(0)
    e2 = Entity(1)
    print(size(Entity))
    print(dprint(e1))
    print(dprint(e2))

