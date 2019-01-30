# example.py using the ecs package
import random
import operator
from bearlibterminal import terminal as term
from spaceship.ecs.map import Map, WORLD

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

class Position(Component):
    Component.counter = mask = Component.counter << 1
    # __slots__ = ['x', 'y', 'z', 'unit']
    def __init__(self, x=0, y=0, z=0, moveable=True):
        self.speed = random.randint(0, 5)
        self.x, self.y, self.z = x, y, z
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


def init_player():
    return Hero(Position(16, 4, 0), Render('@', ORANGE, BLACK), Stats(3))


def init_enemy():
    return Unit(Position(10, 2, 0), Render('@', GREEN, BLACK), Stats(1))


def init_enemy_static():
    return Unit(Position(11, 2, moveable=False), Render('@', GREEN, BLACK), Stats(1))


def random_enemy_move():
    x, y = random.randint(-1, 2), random.randint(-1, 2)
    return x, y


def main():
    room = Map(WORLD)
    hero = init_player()
    unit = init_enemy()
    entities = [hero, unit, init_enemy_static()]
    moves = {
        term.TK_LEFT: (-1, 0),
        term.TK_RIGHT: (1, 0),
        term.TK_UP: (0, -1),
        term.TK_DOWN:(0, 1)
    }
    term.open()
    # term.puts(0, 0, WORLD)
    room.do_fov(hero.position.x, hero.position.y, 7) 
    for x, y, c in room.tiles:
        term.puts(x, y, c)
    for e in entities:
        term.puts(e.position.x, e.position.y, e.render.char)
    term.refresh()
    affected = None
    blocked = None
    stop = False
    while True:
        for e in entities:
            if e.controller:
                ch = term.read()
                if ch in moves.keys():
                    # create a temp position obj to check next if position is blocked
                    p = e.position.copy()
                    p.move(*moves[ch])
                    units_on_pos = any(p == x.position for x in entities if x != e)
                    if not room.blocked(*p) and not units_on_pos:
                        e.position.move(*moves[ch])
                        # movement is complete. Now unit experiences whatever 
                        # tile type. The unit moved onto. Ex. floor does 
                        # nothing Trap does some effects like damage or other
                        affected = room.affects(e)
                    else:
                        if units_on_pos:
                            blocked = "You cannot move there. Your path is blocked by someone."
                        else:
                            blocked = "You cannot move there. Your path is blocked by something."
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
        for x, y, c in room.tiles:
            term.puts(x, y, c)
        for e in entities[::-1]:
            print(e, e.position, room.lit(*e.position))
            if room.lit(*e.position) == 2:
                term.puts(e.position.x, e.position.y, e.render.char)
        print()

        if blocked:
            term.puts(0, 24, blocked)
            blocked = None
        if affected:
            term.puts(0, 24, affected)

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
    # print(Component())

    # p = Hero(position=Position(2, 3, 1),
    #          render=Render('@', WHITE, BLACK),
    #          stats=Stats(3))

    # print(p)
    # print(repr(p))
    # print(p.stats.str, p.stats.health)

    # o = Hero()
    # o.components = Stats(3)
    # o.components = Position(2, 3, 1)
    # o.components = Render('@', '#ffffff', '#000000')

    # q = Unit()
    # q.components = Position(2, 2, 1)
    # q.components = Render('@', WHITE, BLACK)

    # t = Tile()
    # e = Entity()

    # position = Position(0, 0, 0)

    # entities = [p, e, t, o, q]
    # while len(entities) > 3:
    #     entities = TurnSystem(entities)
    #     entities = DamageSystem(entities)
    # print(entities)
    main()
