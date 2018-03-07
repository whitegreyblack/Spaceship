# component.py
from .die import Die

class System:
    def update(self):
        raise NotImplementedError

class Component:
    unit = None
    def __repr__(self):
        '''Returns stat information for dev'''
        return f'{self.__class__.__name__}({self})'

    def __str__(self):
        '''Returns stat information for user'''
        return ", ".join(f'{s}={getattr(self, s)}' for s, a in self.attrs)

    def attr(self, name: str):
        '''Checks if attribute exists and is set'''
        return bool(hasattr(self, name) and getattr(self, name))
    
    @property
    def attrs(self):
        '''Yields attributes that are not None'''
        for a in self.__slots__:
            if self.attr(a):
                yield (a, getattr(self, a))
    
class Description(Component):
    __slots__ = ['unit', 'name', 'less', 'more']
    def __init__(self, name, less=None, more=None):
        self.name = name
        self.less = less
        self.more = more

class Render(Component):
    __slots__ = ['unit', 'symbol', 'foreground', 'background']
    def __init__(self, symbol, foreground="#ffffff", background="#000000"):
        '''Render component that holds all information that allows the map
        to be drawn with correct characters and colors
        >>> r = Render('@')
        >>> r
        Render(symbol=@, foreground=#ffffff, background=#000000)
        >>> r.symbol == '@'
        True
        '''
        self.symbol = symbol
        self.foreground = foreground
        self.background = background

class Attribute(Component):
    __slots__ = ['unit', 'strength', 'agility', 'intelligence']
    def __init__(self, strength, agility, intelligence):
        '''
        >>> Attribute(5, 5, 5)
        Attribute(strength=5, agility=5, intelligence=5)
        '''
        self.strength = strength
        self.agility = agility
        self.intelligence = intelligence

    def update(self):
        if self.unit.has_component('health'):
            self.unit.get_component('health').update()

class Health(Component):
    __slots__ = ['unit', 'max_hp', 'cur_hp']
    def __init__(self, health=0):
        self.max_hp = self.cur_hp = health

    def update(self):
        if self.unit.has_component('attribute'):
            strength = self.unit.get_component('attribute').strength
            self.max_hp = strength * 2 + self.max_hp
            self.cur_hp = strength * 2 + self.cur_hp

class Mana(Component):
    __slots__ = ['unit', 'max_mp', 'cur_mp']
    def __init__(self, mana=0):
        self.max_mp = self.cur_mp = mana

    def update(self):
        if self.unit.has_component('attribute'):
            intelligence = self.unit.get_component('attribute').intelligence
            self.max_mp = intelligence * 2 + self.max_mp
            self.cur_mp = intelligence * 2 + self.cur_mp

class Position(Component):
    __slots__ = ['unit', 'x', 'y', 'ox', 'oy']
    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y

    @property
    def position(self):
        return self.x, self.y

    def move(self, x, y):
        self.x, self.y = self.x + x, self.y + y

    def save(self):
        self.ox, self.oy = self.x, self.y

class Entity:
    '''
    Basic container for entity objects. Holds a list of components which is used
    to represent certain objects in game world.

    >>> e = Entity(components=[Description('hero'),])
    >>> e, Entity.compdict
    (hero, {'description': {0: Description(unit=hero, name=hero)}})
    >>> e.has_component('description')
    True
    >>> e.get_component('description')
    Description(unit=hero, name=hero)
    >>> e.del_component('description')
    >>> e.has_component('description')
    False
    >>> list(e.components())
    []
    '''
    eid = 0
    compdict = {}
    def __init__(self, components=None):
        self.eid = Entity.eid
        Entity.eid += 1
        if components:
            self.add(components=components)

    def __str__(self):
        description = self.get_component('description')
        if description and description.name:
            return description.name
        return str(self.eid)

    def __repr__(self):
        return str(self)

    def __hash__(self):
        return self.eid

    def __eq__(self, other):
        return self.eid == hash(other.eid)
    
    @property
    def components(self):
        for components in self.compdict.values():
            if self.eid in components.keys():
                yield components[self.eid]

    # -- HAS --
    def has(self, name: str=None, names:list=None) -> bool:
        if names:
            return self.has_components(names)
        elif name:
            return self.has_component(name)
        else:
            raise ValueError('No arguments supplied to function: has()')

    def has_component(self, name: str) -> bool:
        if name in self.compdict.keys():
            return self.eid in self.compdict[name].keys()
        return False

    def has_components(self, names: list) -> bool:
        return all([self.has_component(name) for name in names])

    # -- ADD --
    def add(self, component:object=None, components:list=None) -> bool:
        if components:
            self.add_components(components)
        elif component:
            self.add_component(component)

    def add_component(self, component: object) -> None:
        component.unit = self
        name = type(component).__name__.lower()
        if not self.has_component(name):
            try:
                self.compdict[name].update({self.eid: component})
            except:
                self.compdict[name] = {self.eid: component}
            return True
        return False

    def add_components(self, components: list) -> bool:
        for component in components:
            if self.add_component(component):
                if hasattr(component, 'update'):
                    component.update()

    # -- DEL --
    def delete(self, name:str=None, names:list=None) -> None:
        if names:
            self.del_components(names)
        elif name:
            self.del_component(name)
        else:
            raise ValueError('No arguments supplied to function: del()')

    def del_component(self, name: str) -> None:
        if self.has_component(name):
            del self.compdict[name][self.eid]

    def del_components(self, names: list) -> None:
        for name in names:
            self.del_component(name)

    # -- GET --
    def get(self, name:str=None, names:list=None) -> object:
        if names:
            return self.get_components(names)
        elif name:
            return self.get_component(name)

    def get_component(self, name: str) -> object:
        if self.has_component(name):
            return self.compdict[name][self.eid]
        return None

    def get_components(self, names: list) -> list:
        return [component for component 
                in [self.get_component(name) for name in names]
                    if component]

if __name__ == "__main__":
    from doctest import testmod
    testmod()