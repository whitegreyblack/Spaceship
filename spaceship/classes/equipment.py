# equipment.py
from .items import convert
parts=("head", "neck", "body", "arms", "hands", 
        "hand_left", "hand_right", "ring_left", 
        "ring_right", "waist", "legs", "feet")

class Equipment:
    '''Tied to body parts'''
    def __init__(self, parts, equipment=None):
        self.parts = parts
        self.initialize_parts()
        self.weapon_slots = None
        if equipment:
            self.items = equipment

    def initialize_parts(self):
        for part in self.parts:
            setattr(self, part, None)

    @property
    def items(self):
        for part in self.parts:
            yield part, getattr(self, part)

    @items.setter
    def items(self, equipment):
        equipment = [convert(item) for item in equipment]
        for p, part in enumerate(self.parts):
            if equipment[p]:
                self.equip(part, equipment[p])

    def check_part(self, part):
        if isinstance(part, int):
            return self.parts[part]
        return part

    def item_by_part(self, part):
        '''Returns the item at the given body part'''
        part = self.check_part(part)
        item = getattr(self, part)
        if not item:
            yield part, None
        yield part, item

    def stats(self):
        for _, item in self.items:
            if hasattr(item, 'effects'):
                for effect, value in item.effects:
                    yield effect, value

    def stats_by_part(self, part):
        _, item = next(self.item_by_part(part))
        if hasattr(item, 'effects'):
            for effect, value in item.effects:
                yield effect, value

    def equip(self, part, item):
        if not getattr(self, part):
            setattr(self, part, item)
            if hasattr(item, 'hands'):
                print('hands', item.hands)
                self.weapon_slots = item.hands
            return True
        return False

    def unequip(self, part):
        item = getattr(self, part)
        if item:
            setattr(self, part, None)
            yield item
        yield None
