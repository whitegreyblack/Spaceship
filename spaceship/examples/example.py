# example.py using the ecs package
import click
import random
import operator
from bearlibterminal import terminal as term
from ecs.map import Map, EXAMPLES

length = 100

WHITE = "#ffffff"
BLACK = "#000000"
PURPLE = "#8800CC"
YELLOW = "#DDDD00"
ORANGE = "#FF8800"
GREEN = "#00BB00"
BLUE = "#0000BB"
RED = "#BB0000"

map_symbols = {
    '=': ('#003366', '#000000'),
    '.': ('#996633', '#000000'),
    'T': ('#006633', '#000000'),
    '&': ('#006633', '#000000'),
    '-': ('#006699', '#000000'),
    '~': ('#665533', '#000000'),
    '^': ('#BBBBBB', '#000000'),
}

class Component:
    counter = mask = 1
    def __init__(self):
        self.entity = None

    def __str__(self):
        if isinstance(self, tuple(Component.__subclasses__())):
            parent = type(self).__base__.__name__
            child = type(self).__name__
            return f'{parent}: {child}'

        subclasses = "\n\t   ".join([s.__name__ for s in self.subclasses()])
        return f'{type(self).__name__}: {subclasses}'

    @property
    def name(self):
        return self.__class__.__name__.lower()

    def subclasses(self):
        for s in Component.__subclasses__():
            yield s

    def chain(self, unit):
        self.unit = unit

    def copy(self):
        c = self.__class__()
        c.entity = self.entity
        return c

class Position(Component):
    Component.counter = mask = Component.counter << 1
    attrs = ('x', 'y', 'moveable')
    
    def __init__(self, x=0, y=0, moveable=True):
        self.x, self.y = x, y
        self.moveable = moveable
    
    def __str__(self):
        return f"Position: ({self.x}, {self.y})"
    
    def __iter__(self):
        return iter((self.x, self.y))
    
    def __eq__(self, other):
        return (self.x, self.y) == (other.x, other.y)
    
    def move(self, x, y):
        if self.moveable:
            self.x += x
            self.y += y

    def copy(self):
        """
        Returns a new Position instance with the same property values as the 
        current instance being copied.
        """
        return Position(self.x, self.y, moveable=self.moveable)
        
class Render(Component):
    Component.counter = mask = Component.counter << 1
    # __slots__ = ['char', 'fore', 'back', 'unit']
    def __init__(self, c, f=None, b=None):
        self.char, self.fore, self.back = c, f, b

    @property
    def char(self):
        c = self._c
        if self.fore:
            c = f"[color={self.fore}]{c}[/color]"
        if self.back:
            c = f"[bkcolor={self.back}]{c}[/bkcolor]"
        return c

    @char.setter
    def char(self, c):
        self._c = c

class Controller(Component):
    Component.counter = mask = Component.counter << 1

class Stats(Component):
    Component.counter = mask = Component.counter << 1

    def __init__(self, s):
        self.str = s
        self.health = s

    @property
    def health(self):
        return self._health

    @health.setter
    def health(self, value):
        self._health = value
        # if self._health <= 0:
        #     del self.entity
    
class Entity:
    """Base entity class. All other 'unit' classes derive from this."""
    obj_id = 0
    obj_mask = 0

    def __init__(self): 
        self.obj_id = Entity.obj_id
        Entity.obj_id += 1

    def __str__(self):
        return f"{type(self).__name__}({self.obj_id})"

    def __repr__(self):
        components = ", ".join([c for c in self.components])
        return f"{self}{(': (' + components + ')') if components else ''}"

    def __hash__(self):
        return self.obj_id

    def __eq__(self, other):
        return self.obj_id == hash(other.obj_id)

    @property
    def components(self):
        for component in self.__dict__:
            if isinstance(getattr(self, component), Component):
                yield component

    @components.setter
    def components(self, component):
        name = type(component).__name__.lower()
        if hasattr(self, name) and getattr(self, name):
            raise ValueError('Cannot add a second component of same type')
        setattr(self, name, component)
        self.mask = component
        component.chain(self)

    @property
    def mask(self):
        return self.obj_mask

    @mask.setter
    def mask(self, component):
        self.obj_mask |= component.mask

class Unit(Entity):
    controller = None
    
    def __init__(self, *components):
        super().__init__()
        for component in components:
            component.entity = self
            setattr(self, component.name, component)


class Hero(Unit):
    controller = Controller()


def walk(world, unit):
    x, y = random.randint(-1, 1), random.randint(-1, 1)
    try:
       tile = world[y+unit.y][x+unit.x]
    except IndexError:
        x, y = 0, 0
    else:
        if tile == ".":
            return x, y
        else:
            return 0, 0
       
class Tile(Entity):
    render = None
    
def TurnSystem(entities):
    component='position'
    movables = sorted(
        (e for e in entities 
            if hasattr(e, component) and getattr(e, component)
        ),
        key=operator.attrgetter('position.speed')
    )

    for e in movables:
        print(e, e.position.speed)

    return entities

def DamageSystem(entities):
    component = 'stats'
    damageables = [
        e for e in entities 
            if hasattr(e, component) and getattr(e, component)
    ]
    removables = []
    for e in damageables:
        # h = e.stats.health
        # e.stats.health = random.randint(0, 1)
        # print(h, e.stats.health)
        if e.stats.health <= 0:
            removables.append(e)
    
    for e in removables:
        entities.remove(e)

    return entities


def init_player(floors):
    p = next(floors)
    return Hero(Position(*p), Render('@', ORANGE, BLACK), Stats(3))


def init_enemy(floors):
    p = next(floors)
    return Unit(Position(*p), Render('@', GREEN, BLACK), Stats(1))


def init_enemy_static(floors):
    p = next(floors)
    return Unit(
        Position(*p, moveable=False), 
        Render('@', GREEN, BLACK), 
        Stats(1)
    )

def within(width, height, ux, uy):
    return 0 <= ux < width and 0 <= uy < height

def random_enemy_move():
    x, y = random.randint(-1, 2), random.randint(-1, 2)
    return x, y

@click.command()
@click.option('--size', default="r", help="size of room")
def main(size):
    """
    Runs a basic loop using blt and several game objects representing a subset
    of actions available in the full application.
    """
    term.open()
    
    width, height = term.state(term.TK_WIDTH), term.state(term.TK_HEIGHT)
    print(term.state(term.TK_WIDTH), term.state(term.TK_HEIGHT))

    turns = 0

    # basic game objects
    room = Map(EXAMPLES[size.upper()])
    floors = iter(room.floors)
    hero = init_player(floors)
    entities = [hero, init_enemy(floors), init_enemy_static(floors)]

    # our current action list, limited to movements only
    moves = {
        term.TK_LEFT: (-1, 0),
        term.TK_RIGHT: (1, 0),
        term.TK_UP: (0, -1),
        term.TK_DOWN:(0, 1)
    }

    # term.puts(0, 0, WORLD)
    room.do_fov(hero.position.x, hero.position.y, 7) 

    for x, y, c in room.output(*hero.position, width//2, height//2):
        term.puts(x, y, c)

    for e in entities:
        inbounds = within(width, height, *e.position)
        visible = room.lit(*e.position) == room.FULL_VISIBLE
        if inbounds and visible:
            term.puts(*e.position, e.render.char)

    term.puts(0, 24, f"turns: {turns}")
    term.refresh()
    affected = None
    blocked = None
    stop = False

    # game loop
    while True:
        for e in entities:
            # differentiate actions based on controller components
            if e.controller:
                ch = term.read()

                # action keys allow character to move
                if ch in moves.keys():
                    # create a temp position object to check if position is 
                    # blocked
                    p = e.position.copy()
                    p.move(*moves[ch])
                    units_on_pos = any(
                        p == x.position for x in entities if x != e
                    )

                    # if no map object or unit object in the position we wnat
                    # to move to, finally move the real entity.
                    if not room.blocked(*p) and not units_on_pos:
                        e.position.move(*moves[ch])
                        # movement is complete. Now unit experiences whatever 
                        # tile type. The unit moved onto. Ex. floor does 
                        # nothing Trap does some effects like damage or other
                        affected = room.affects(e)
                    else:
                        if units_on_pos:
                            blocked = "You cannot move there. \
                                Your path is blocked by someone."
                        else:
                            blocked = "You cannot move there. \
                                Your path is blocked by something."

                if ch == term.TK_CLOSE or ch == term.TK_ESCAPE:
                    stop = True
                    break
            else:
                p = e.position.copy()
                if p.moveable:
                    p.move(*random_enemy_move())
                    if not room.blocked(*p):
                        e.position = p.copy()
        if stop:
            break

        term.clear()
        room.do_fov(hero.position.x, hero.position.y, 7)

        for x, y, c in room.output(*hero.position, width//2, height//2):
            term.puts(x, y, c)
        
        for e in entities[::-1]:
            inbounds = within(width, height, *e.position)
            visible = room.lit(*e.position) == room.FULL_VISIBLE
            if inbounds and visible:
                term.puts(*e.position, e.render.char)

        if blocked:
            term.puts(0, 24, blocked)
            blocked = None
        
        if affected:
            term.puts(0, 24, affected)
        
        term.puts(0, 24, f"turns: {turns}")
        entities = DamageSystem(entities)
        
        if hero not in entities:
            term.clear_area(0, 24, 79, 24)
        
            if affected:
                term.puts(0, 23, affected)

            term.puts(0, 24, "You die.")
            term.refresh()
            term.read()
            break
        
        term.refresh()
    
    term.close()

if __name__ == "__main__":
    main()
