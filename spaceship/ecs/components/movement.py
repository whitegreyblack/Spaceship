# movement.py

"""Experience component"""

from dataclasses import dataclass

from .component import Component


@dataclass
class Movement(Component):
    x: int
    y: int

if __name__ == "__main__":
    from ecs.utis import dprint
    m = Movement(1, 1)
    print(dprint(e))
