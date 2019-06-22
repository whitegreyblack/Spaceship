# component.py

"""Component classes"""

from dataclasses import dataclass, field


@dataclass
class Component(object):
    """
    Base component class that defines subclass agnostic methods
    """
    __slots__ = []

    def __repr__(self):
        attributes = [ 
            f"{s}={getattr(self, s)}"
                for s in self.__slots__
                    if bool(hasattr(self, s) and getattr(self, s) is not None)
        ]
        attr_string = ", ".join(attributes)
        return f"{self.__class__.__name__}({attr_string})"

    @classmethod
    def classname(cls):
        return cls.__name__.lower()


@dataclass
class AI(Component):
    ...


@dataclass
class Collision(Component):
    entity_id: int = -1
    x: int = 0
    y: int = 0


@dataclass
class Effect(Component):
    char: str
    foreground: str = None
    background: str = None
    ticks: int = 1


@dataclass
class Experience(Component):
    level: int = 1
    exp: int = 0


@dataclass
class Health(Component):
    max_hp: int = 1
    cur_hp: int = 1
    @property
    def alive(self):
        return self.cur_hp > 0


@dataclass
class Information(Component):
    name: str


@dataclass
class Movement(Component):
    x: int
    y: int


@dataclass
class Position(Component):
    x: int = 0
    y: int = 0
    moveable: bool = True
    blocks_movement: bool = True


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
    for component in Component.__subclasses__():
        try:
            print(component())
        except TypeError:
            pass
