# component.py

"""Base component class"""

from dataclasses import dataclass


@dataclass
class Component(object):
    """
    Base component class that defines subclass agnostic methods
    """
    __slots__ = []

    def __repr__(self):
        attributes = [ 
            f"{s}={getattr(self, s)}"
                for s in self.__slots__
                    if bool(hasattr(self, s) and getattr(self, s) is not None)
        ]
        attr_string = ", ".join(attributes)
        return f"{self}({attr_string})"

    def __str__(self):
        return f'{self.__class__.__name__}'

    @classmethod
    def classname(cls):
        return cls.__name__.lower()

    # def __hash__(self):
    #     return hash(self.id)

    # def __eq__(self, other):
    #     return self.id == other.id

    # @staticmethod
    # def join(cls, other, *others):
    #     return set.intersection(cls.instances, 
    #                             other.instances,
    #                             *(o.instances for o in others))

    # @property
    # def classname(self):
    #     return self.__name__.lower()

    # @classmethod
    # def items(cls):
    #     return cls.instances

if __name__ == "__main__":
    from ecs.util import dprint
    c = Component()
    print(dprint(c))
