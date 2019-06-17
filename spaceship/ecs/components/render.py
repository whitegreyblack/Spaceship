# render.py

"""Render component"""

from dataclasses import dataclass

from .component import Component


@dataclass
class Render(Component):
    char: str = '@'
    fore: str = None #'#ffffff'
    back: str = None #'#000000'

    @property
    def string(self):
        if self.fore:
            return self.fore + self.char
        return self.char

if __name__ == "__main__":
    from ecs.util import dprint
    r = Render()
    g = Render()
    b = Render()
    print(dprint(r))
    print(dprint(g))
    print(dprint(b))
