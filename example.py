length = 100
world = '''\
################################
#....#....#....#....#..........#
#...................#..........#
#....#....#....#....+.....#....#
#...................#..........#
#....#....#....#....#..........#
################################
'''[1:]
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
    comp_mask = 0x0
    def __str__(self):
        if isinstance(self, tuple(Component.__subclasses__())):
            parent = self.__class__.__base__.__name__
            child = self.__class__.__name__
            return f'{parent}: {child}'
        return f'{self.__class__.__name__}: Base'

class Position(Component):
    comp_mask = 0x1
    __slots__ = ['x', 'y', 'z', 'unit']
    def __init__(self, unit, x, y, z):
        self.unit = unit
        self.x, self.y, self.z = x, y, z

class Render(Component):
    comp_mask = 0x2
    __slots__ = ['char', 'fore', 'back', 'unit']
    def __init__(self, unit, c, f, b):
        self.unit = unit
        self.char, self.fore, self.back = c, f, b

class Entity:
    class_id = 0
    class_mask = 0
    def __init__(self):
        Entity.class_id += 1
    
    def add_component(self, component):
        name = component.__class__.__name__.lower()
        if hasattr(self, name):
            raise ValueError('Cannot add a second component of same type')
        setattr(self, name, component)
    
class Player(Entity):
    position = None
    render  = None

    def add_component(self, component):
        self.class_mask |= component.comp_mask
        name = component.__class__.__name__.lower()
        if hasattr(self, name) and getattr(self, name):
            raise ValueError('Cannot add a second component of same type')
        setattr(self, name, component)

if __name__ == "__main__":
    p = Player()
    print(p.class_mask)
    print(p.position, p.render)
    p.add_component(Position(p, 2, 3, 1))
    print(p.position, p.class_mask)
    p.add_component(Render(p, '@', '#ffffff', '#000000'))
    print(p.render, p.class_mask)
    print(p.class_id)

    e = Entity()
    print(e.class_id)

    q = Player()
    print(q.class_id)

    position = Position(None, 0, 0, 0)
    print(position)