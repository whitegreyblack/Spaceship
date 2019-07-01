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
    manager: str = 'ais'


@dataclass
class Collision(Component):
    entity_id: int = -1
    x: int = 0
    y: int = 0
    manager: str = 'collisions'


@dataclass
class Destroy(Component):
    manager: str = 'destroyed'


@dataclass
class Effect(Component):
    char: str
    foreground: str = None
    background: str = None
    ticks: int = 1
    manager: str = 'effects'


@dataclass
class Experience(Component):
    level: int = 1
    exp: int = 0
    manager: str = 'experiences'


@dataclass
class Health(Component):
    cur_hp: int = 1
    max_hp: int = 1
    manager: str = 'healths'
    @property
    def alive(self):
        return self.cur_hp > 0


@dataclass
class Input(Component):
    is_player: bool = False
    manager: str = 'inputs'


@dataclass
class Information(Component):
    name: str
    manager: str = 'infos'


@dataclass
class Movement(Component):
    x: int
    y: int
    manager: str = 'movements'
    @classmethod
    def from_input(cls, keypress):
        directions = {
            'down': ( 0,  1),
            'up': ( 0, -1),
            'left': (-1,  0),
            'right': ( 1,  0),
        }
        return cls(*directions[keypress])


@dataclass
class Openable(Component):
    opened: bool = False
    manager: str = 'openables'


@dataclass
class Position(Component):
    x: int = 0
    y: int = 0
    moveable: bool = True
    blocks_movement: bool = True
    manager: str = 'positions'
    def __eq__(self, other):
        return (self.x, self.y) == (other.x, other.y)


@dataclass
class Render(Component):
    char: str = '@'
    fore: str = None #'#ffffff'
    back: str = None #'#000000'
    manager: str = 'renders'
    @property
    def string(self):
        if self.fore:
            return self.fore + self.char
        return self.char


@dataclass
class Tile(Component):
    entity_id: int
    manager: str = 'tiles'


@dataclass
class TileMap(Component):
    width: int
    height: int
    manager: str = 'tilemaps'


@dataclass
class Visibility(Component):
    level: int = 0
    manager = 'visibilities'


@dataclass
class Inventory(Component):
    size: int = 10
    items: list = field(default_factory=list)
    manager = 'inventories'

@dataclass
class Item(Component):
    manager = 'items'

components = Component.__subclasses__()

if __name__ == "__main__":
    from ecs.debug import dprint
    for component in Component.__subclasses__():
        try:
            print(component())
        except TypeError:
            pass
