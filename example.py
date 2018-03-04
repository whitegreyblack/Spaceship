import random
import operator
from bearlibterminal import terminal as term
length = 100
world = '''
################################
#....#....#....#....#..........#
#...................#..........#
#....#....#....#....+.....#....#
#...................#..........#
#....#....#....#....#..........#
################################
'''[1:]
WHITE = "#ffffff"
BLACK = "#000000"
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
    mask = 0x0
    def __str__(self):
        if isinstance(self, tuple(Component.__subclasses__())):
            parent = type(self).__base__.__name__
            child = type(self).__name__
            return f'{parent}: {child}'

        subclasses = "\n\t   ".join([s.__name__ for s in self.subclasses()])
        return f'{type(self).__name__}: {subclasses}'

    def subclasses(self):
        for s in Component.__subclasses__():
            yield s

    def chain(self, unit):
        self.unit = unit

class Position(Component):
    mask = 0x1
    # __slots__ = ['x', 'y', 'z', 'unit']
    def __init__(self, x=0, y=0, z=0):
        self.speed = random.randint(0, 5)
        self.x, self.y, self.z = x, y, z
        
class Render(Component):
    mask = 0x2
    # __slots__ = ['char', 'fore', 'back', 'unit']
    def __init__(self, c, f, b):
        self.char, self.fore, self.back = c, f, b

class Controller(Component):
    mask = 0x3

class Stats(Component):
    mask = 0x4

    def __init__(self, s):
        self.str = s
        self.health = s * 3
    
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

class Hero(Entity):
    stats = None
    position = None
    render  = None
    controller = None

    def __init__(self, position=None, render=None, controller=None, stats=None):
        super().__init__()
        for component in [position, render, controller, stats]:
            if component:
                self.components = component
        
class Unit(Entity):
    health = None
    position = None
    render = None
    controller = None
    
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
    movables = sorted((e for e in entities 
                         if hasattr(e, component) and getattr(e, component)),
                      key=operator.attrgetter('position.speed'))

    for e in movables:
        print(e, e.position.speed)

    return entities

def DamageSystem(entities):
    component = 'stats'
    damageables = list(e for e in entities 
                         if hasattr(e, component) and getattr(e, component))
    removables = []
    for e in damageables:
        h = e.stats.health
        e.stats.health = random.randint(0, 1)
        print(h, e.stats.health)
        if e.stats.health <= 0:
            removables.append(e)
    
    for e in removables:
        entities.remove(e)

    return entities

def init_player():
    return Hero(position=Position(16, 4, 0),
                render=Render('@', WHITE, BLACK),
                stats=Stats(3))

def init_enemy():
    return Hero(position=Position(10, 2, 0),
                render=Render('@', WHITE, BLACK),
                stats=Stats(1))


def main():
    hero = init_player()
    unit = init_enemy()
    entities = [hero, unit]
    term.open()
    term.puts(0, 0, world)
    for e in entities:
        term.puts(e.position.x, e.position.y, e.render.char)
    term.refresh()
    term.read()
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