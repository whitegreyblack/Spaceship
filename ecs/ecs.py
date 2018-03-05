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

    >>> import components
    >>> e = Entity(description=components.Description('hero'))
    >>> e
    hero(0): 
    >>> print(e)
    hero
    >>> hash(e)
    0
    '''
    eid = 0
    def __init__(self, description, components=None):
        self.eid = Entity.eid
        Entity.eid += 1
        self.description = description
        if components:
            for name, component in components.items():
                self.add_component(name, component)

    def __str__(self):
        return self.description.name

    def __repr__(self):
        return f"{self}({self.eid}): {', '.join(str(c) for c in self.components)}"

    def __hash__(self):
        return self.eid

    def __eq__(self, other):
        return self.eid == hash(other.eid)
    
    @property
    def components(self):
        for component in self.__dict__:
            if isinstance(getattr(self, component), Component):
                yield self.__dict__[component]

    def has_component(self, name):
        return bool(hasattr(self, name) and getattr(self, name))

    def add_component(self, name, component):
        if not self.has_component(name):
            setattr(self, name, component)

    def del_component(self, name):
        if self.has_component(self, name):
            delattr(self, name)

    def get_component(self, name, component):
        if self.has_component(self, name):
            return getattr(self, name)

if __name__ == "__main__":
    from doctest import testmod
    testmod()