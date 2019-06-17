# collision.py

"""Collision component"""

from dataclasses import dataclass

from .component import Component


@dataclass
class Collision(Component):
    collided_entity_id: int

if __name__ == "__main__":
    from ecs.util import dprint
    c = Collision(1)
    print(dprint(c))
