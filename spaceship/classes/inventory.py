# inventory.py
from .items import convert

class Inventory(list):
    '''Regular list'''
    def __init__(self, items):
        super().__init__()
        self.extend([convert(item) for item in items])

    def by_type(self, part):
        for item in self:
            if hasattr(item, 'placement'):
                if part in item.placement:
                    yield item

    def by_prop(self, prop):
        for item in self:
            if hasattr(item, prop):
                yield item

    def add(self, item):
        if len(self) <= 25:
            self.append(item)
            return True
        else:
            return False

    @property
    def items(self):
        for group, items in sort(self).items():
            if group not in 'food others'.split():
                group = list(group + 's')
                group[0] = group[0].upper()
                group = "".join(group)
            yield group, items

if __name__ == "__main__":
    print(__file__)