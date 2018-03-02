# entity.py

from component import Component
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

if __name__ == "__main__":
    from doctest import testmod
    testmod()