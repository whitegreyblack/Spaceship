# experience.py

"""Experience component"""

from dataclasses import dataclass

from .component import Component


@dataclass
class Experience(Component):
    level: int = 1
    exp: int = 0

if __name__ == "__main__":
    from ecs.util import dprint
    e = Experience()
    print(dprint(e))
