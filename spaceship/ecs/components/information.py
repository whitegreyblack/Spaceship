# information.py

"""Information component"""

from dataclasses import dataclass
from dataclasses import field
from .component import Component

@dataclass
class Information(Component):
    name: str

if __name__ == "__main__":
    from ecs.util import dprint
    i = Information("the entity")
    print(dprint(i))
