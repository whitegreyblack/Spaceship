# AI.py

"""AI component"""

from dataclasses import dataclass

from .component import Component


@dataclass
class AI(Component):
    ...

if __name__ == "__main__":
    from ecs.util import dprint
    a = AI()
    print(dprint(a))
