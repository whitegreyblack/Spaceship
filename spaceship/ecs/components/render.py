# render.py

"""Render component"""

from dataclasses import dataclass

from .component import Component


@dataclass
class Render(Component):
    char: str = '@'
    fore: str = '#ffffff'
    back: str = '#000000'

if __name__ == "__main__":
    from ecs.util import dprint
    r = Render()
    print(dprint(r))
