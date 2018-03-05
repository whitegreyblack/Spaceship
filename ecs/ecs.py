# component.py
from die import Die

class Component:
    def __str__(self):
        return f"{type(self).__name__}: ({', '.join(next(self.attrs))})"

    def __repr__(self):
        return f"{type(self).__name__}: ({', '.join(next(self.attrs))})"
        
    def attr(self, name):
        return bool(hasattr(self, name) and getattr(self, name))
    
    @property
    def attrs(self):
        yield (f"'{getattr(self, a)}'" for a in self.__slots__ if self.attr(a))
    # def __str__(self):
    #     if isinstance(self, tuple(Component.__subclasses__())):
    #         parent = type(self).__base__.__name__
    #         child = type(self).__name__
    #         return f'{parent}: {child}'

    #     subclasses = "\n\t   ".join([s.__name__ for s in self.subclasses()])
    #     return f'{type(self).__name__}: {subclasses}'

    # def subclasses(self):
    #     for s in Component.__subclasses__():
    #         yield s

    # def chain(self, entity):
    #     self.entity = entity

    # def eval_dice_strings(string):
    #     string_single = isinstance(strings, str)
    #     if string_single:
    #         strings = strings.split()
        
    #     if string_single or all([isinstance(s, str) for s in strings]):
    #         strings = [next(Die.construct(stat).roll()) for stat in strings]
        
    #     return strings

class Entity:
    '''
    Basic container for entity objects. Holds a list of components which is used
    to represent certain objects in game world.

    >>> e = Entity('hero')
    >>> e
    hero(0)
    >>> print(e)
    hero
    >>> hash(e)
    0
    '''
    eid = 0
    def __init__(self, name):
        self.name = name
        self.eid = Entity.eid
        Entity.eid += 1

    def __repr__(self):
        return f'{self.name}({self.eid})'

    def __str__(self):  
        return self.name

    def __hash__(self):
        return self.eid

    def __eq__(self, other):
        return self.eid == hash(other.eid)
    
    @property
    def components(self):
        for component in self.__dict__:
            if isinstance(getattr(self, component), Component):
                yield self.__dict__[component]

    @components.setter
    def components(self, component):
        name = type(component).__name__.lower()
        if hasattr(self, name) and getattr(self, name):
            raise ValueError('Cannot add a second component of same type')

        setattr(self, name, component)
        component.chain(self)

    def has_component(self, name):
        return bool(hasattr(self, name) and getattr(self, name))

    def add_component(self, name, component):
        if not self.has_component(name):
            setattr(self, name, component)

    def del_component(self, name):
        if self.has_component(self, name):
            delattr(self, name)

if __name__ == "__main__":
    from doctest import testmod
    testmod()