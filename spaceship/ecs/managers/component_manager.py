# componentmanager.py

"""Base class for component manager"""

# TODO: should we allow duplicate entity?

from dataclasses import dataclass, field


def join(*managers):
    # at least two needed
    if len(managers) == 1:
        return managers.components.items()
    first, *rest = managers
    keys = set(first.components.keys())
    for manager in rest:
        keys = keys.intersection(set(manager.components.keys()))
    for eid in keys:
        yield eid, (m.components[eid] for m in managers)

class ComponentManager(object):

    __slots__ = ['ctype', 'components']

    def __init__(self, ctype):
        self.ctype = ctype.__name__
        self.components = dict()

    def __str__(self):
        l = len(self.components.keys())
        return f"{self.__class__.__name__}(components={l})"

    def __iter__(self):
        for k, v in self.components.items():
            yield k, v

    def __contains__(self, eid):
        return eid in self.components.keys()

    # def join(self, *others):
    #     keys = set(self.components.keys())
    #     for other in others:
    #         keys =  keys.intersection(set(other.components.keys()))
    #     for eid in keys:
    #         builder = []
    #         for manager in (self, *others):
    #             builder.append(manager.components[eid])
    #         yield eid, builder

    def exclude(self, other):
        for eid, component in self:
            if eid not in other:
                yield eid, component

    def add(self, entity, component):
        if type(component).__name__ is not self.ctype:
            raise ValueError("Invalid component type added.")
        self.components[entity.id] = component

    def remove(self, entity) -> bool:
        if entity.id in self.components:
            del self.components[entity.id]
            return True
        return False

    def find(self, entity):
        # print(self.ctype, entity, self.components)
        if entity.id in self.components.keys():
            return self.components[entity.id]
        return None

if __name__ == "__main__":
    from util import dprint, gso
    c = ComponentManager()
    print(dprint(c))
