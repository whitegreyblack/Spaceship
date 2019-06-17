# position.py

"""Position component"""

from dataclasses import dataclass

from .component import Component


@dataclass
class Position(Component):
    x: int = 0
    y: int = 0
    moveable: bool = True

if __name__ == "__main__":
    from ecs.util import dprint, gso
    p = Position(0, 0)
    print(dprint(p))
