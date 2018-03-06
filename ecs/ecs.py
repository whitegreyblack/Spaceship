# component.py
from die import Die

class System:
    def update(self):
        raise NotImplementedError

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
    >>> e = Entity(components=[components.Description('hero'),])
    >>> e, Entity.compdict
    (0, {'description': {0: Description: ('hero')}})
    >>> e.has_component('description')
    True
    >>> e.get_component('description')
    Description: ('hero')
    >>> e.del_component('description')
    True
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
            for component in components:
                self.add_component(component)

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
    
    def components(self):
        for components in self.compdict.values():
            if self.eid in components.keys():
                yield components[self.eid]

    def has_component(self, name: str) -> bool:
        if name in self.compdict.keys():
            return self.eid in self.compdict[name].keys()
        return False

    def add_component(self, component: object) -> bool:
        name = type(component).__name__.lower()
        if not self.has_component(name):
            try:
                self.compdict[name].update({self.eid: component})
            except:
                self.compdict[name] = {self.eid: component}
            return True
        return False

    def del_component(self, name: str) -> bool:
        if self.has_component(name):
            del self.compdict[name][self.eid]
            return True
        return False
            
    def get_component(self, name: str) -> object:
        if self.has_component(name):
            return self.compdict[name][self.eid]
        return False

if __name__ == "__main__":
    from doctest import testmod
    testmod()