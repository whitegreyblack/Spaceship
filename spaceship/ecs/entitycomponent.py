# entity.py

from ecs import Component

class EntityComponents:
    """
    Basic container for entity objects. Holds a list of components which is used
    to represent certain objects in game world.
    """
    # __slots__ = ['eid', 'delete', 'ai', 'moveable', 'race'] + [
    #     sc.classname() for sc in Component.__subclasses__()
    # ]
    __slots__ = ['eid', 'components']
    EID = 0
    # instances = {}
    # compdict = {c.__name__.lower(): {} for c in Component.__subclasses__()}
    def __init__(self, components=None):
        self.eid = Entity.EID
        Entity.EID += 1
        # self.FLAG = 0
        self.components = dict()
        self.components['delete'] = False
        if components:
            if not isinstance(components, list):
                components = [components]
            for component in components:
                if isinstance(component, Component):
                    self.__setattr__(component.classname(), component)
                else:
                    self.__setattr__(*component)

    def __new__(cls, components=None):
        if components:
            if not isinstance(components, list):
                components = [components]
        return object.__new__(cls)

    def __str__(self):
        return str(self.eid)

    def __repr__(self): 
        components = "\n".join(f"{key}: {repr(value)}"
            for key, value in self.components.items())
        return f"Entity(eid={self})\n{components}"

    def __hash__(self): 
        return self.eid

    def __eq__(self, other): 
        return self.eid == hash(other.eid)

    def __lt__(self, other): 
        return self.eid < hash(other.eid)

    def __getattr__(self, key):
        # check first level order keys: match eid or components
        if key in self.__slots__:
            return super(Entity, self).__getattr__(key)
        # check second level order keys in self.components: match comp name
        if key in self.components:
            return self.components[key]
        for component in self.components.values():
            # check third level order keys in individual components: ex symbol
            if isinstance(component, Component) and key in component.__slots__:
                return getattr(component, key)

    def __setattr__(self, key, value):
        if isinstance(value, Component):
            value.unit = self
        if key in self.__slots__:
            super(Entity, self).__setattr__(key, value)
            return
        for component in self.components.values():
            if isinstance(component, Component) and key in component.__slots__:
                setattr(component, key, value)
                return
        self.components[key] = value
        # raise ValueError(f"Entity has no attribute {key}")
    # # ? should I move these into components?
    # @property
    # def components(self):
    #     for component in self.components:
    #         if hasattr(self, component) and getattr(self, component) is not None:
    #             if component in Component.__subclasses__():
    #                 yield repr(getattr(self, component))
    #             else:
    #                 yield f"{component}={getattr(self, component)}"

    # # -- HAS --
    # def has(self, name: str=None, names:list=None) -> bool:
    #     if names:
    #         return self.has_components(names)
    #     elif name:
    #         return self.has_component(name)
    #     else:
    #         raise ValueError('No arguments supplied to function: has()')

    # def has_component(self, name: str) -> bool:
    #     if name in self.compdict.keys():
    #         return self.eid in self.compdict[name].keys()
    #     return False

    # def has_components(self, names: list) -> bool:
    #     return all([self.has_component(name) for name in names])

    # # -- ADD --
    # def add(self, component:object=None, components:list=None) -> bool:
    #     if components:
    #         self.add_components(components)
    #     elif component:
    #         self.add_component(component)
    #     else:
    #         raise ValueError('No arguments supplied to function: add()')
   
    # def add_component(self, component: object) -> None:
    #     component.unit = self
    #     name = type(component).__name__.lower()
    #     if not self.has_component(name):
    #         # try:
    #         self.compdict[name].update({self.eid: component})
    #         self.FLAG |= component.FLAG
    #         # except:
    #             # self.compdict[name] = {self.eid: component}
    #         return True
    #     return False

    # def add_components(self, components: list) -> bool:
    #     for component in components:
    #         if self.add_component(component):
    #             if hasattr(component, 'update'):
    #                 component.update()

    # # -- DEL --
    # def delete(self, name:str=None, names:list=None) -> None:
    #     if names:
    #         self.del_components(names)
    #     elif name:
    #         self.del_component(name)
    #     else:
    #         raise ValueError('No arguments supplied to function: del()')

    # def del_component(self, name: str) -> None:
    #     if self.has_component(name):
    #         del self.compdict[name][self.eid]

    # def del_components(self, names: list) -> None:
    #     for name in names:
    #         self.del_component(name)

    # # -- GET --
    # def get(self, name:str=None, names:list=None) -> object:
    #     if names:
    #         return self.get_components(names)
    #     elif name:
    #         return self.get_component(name)
    #     else:
    #         raise ValueError('No arguments supplied to function: get()')

    # def get_component(self, name: str) -> object:
    #     if self.has_component(name):
    #         return self.compdict[name][self.eid]
    #     return None

    # def get_components(self, names: list) -> list:
    #     return [component for component 
    #             in [self.get_component(name) for name in names]
    #                 if component]

if __name__ == "__main__":
    e = Entity()
    print(e)
    print(e.eid)
