# component.py

class Component:
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

    def chain(self, entity):
        self.entity = entity