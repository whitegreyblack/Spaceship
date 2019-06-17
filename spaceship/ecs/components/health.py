# health.py

"""Health component"""

from dataclasses import dataclass

from .component import Component


@dataclass
class Health(Component):
    max_hp: int = 1
    cur_hp: int = 1

if __name__ == "__main__":
    from ecs.util import dprint
    h = Health()
    print(dprint(h))
