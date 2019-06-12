# component.py
from bearlibterminal import terminal as term
import random
from ecs.die import Die, check_sign as check

def roll(value):
    if isinstance(value, str):
        return next(Die.construct(value).roll)
    return value

class System:
    def update(self):
        raise NotImplementedError

'''
# Component Definitions
Unit: -> if entity has these components -- it is a unit
    Render | Information | Position | Equipment | Inventory
Weapon:
    Render | Information | Position(optional) | Damage
Armor:
    Render | Information | Position(optional) | Defense
'''
class Component(object):
    '''Base Parent Class to implement widely used class methods'''
    def __repr__(self):
        '''Returns stat information for dev'''
        component_variables = ", ".join(
            f'{s}={getattr(self, s)}' 
                for s in self.__slots__
                    if s != "unit"
                        and bool(hasattr(self, s) 
                        and getattr(self, s))
        )
        return f'{self}({component_variables})'

    def __str__(self):
        '''Returns stat information for user'''
        return f'{self.__class__.__name__}'

    def __hash__(self):
        return hash(self.id)

    def __eq__(self, other):
        return self.id == other.id

    @staticmethod
    def join(cls, other, *others):
        '''Should either return the entities or entity_ids'''
        return set.intersection(cls.instances, 
                                other.instances,
                                *(o.instances for o in others))

    @classmethod
    def classname(cls):
        return cls.__name__.lower()

    @classmethod
    def items(cls):
        return cls.instances

class Ai(Component):
    __slots__ = ['unit', 'ai']
    instances = set()
    def __init__(self):
        self.ai = True

class Render(Component):
    __slots__ = ['unit', 'symbol', 'foreground', 'background']
    instances = set()
    def __init__(self, symbol, foreground="#ffffff", background="#000000"):
        '''Render component that holds all information that allows the map
        to be drawn with correct characters and colors
        >>> r = Render('@')
        >>> r
        Render(symbol=@, foreground=#ffffff, background=#000000)
        >>> r.symbol == '@'
        True
        '''
        self.symbol = symbol
        self.foreground = foreground
        self.background = background

    def __call__(self):
        return self.background, f"[c={self.foreground}]{self.symbol}[/c]"

class Position(Component):
    __slots__ = ['unit', 'x', 'y']
    instances = set()
    def __init__(self, x=0, y=0, moveable=True):
        self.x = x
        self.y = y
        self.moveable = moveable

    def __call__(self):
        return self.x, self.y

class Information(Component):
    instances = set()
    __slots__ = ['unit', 'name', 'race', 'gender']

    def __init__(self, name=None, race=None, gender=None):
        if not name and not race:
            raise ValueError("Need at least a name or race")

        for atr, val in zip(self.__slots__[1:], [name, race, gender]):
            setattr(self, atr, val if val else None)

    def __call__(self):
        return self.name if self.name else self.race

class Inventory(Component):
    instances = set()
    __slots__ = ['unit', 'bag']

    def __init__(self, bag=[]):
        self.max = 26
        self.bag = bag

class Delete(Component):
    instances = set()
    __slots__ = ['unit', 'delete']

    def __init__(self):
        self.delete = True

    def empty(bag): 
        return len(bag) == 0

    def full(bag, size): 
        return len(bag) == size

    def pickup(bag, item, size):
        if len(bag) < size:
            return False
        bag.append(item)
        return True

    def drop(bag, item):
        if len(bag) == 0:
            return False
        bag.remove(item)
        return True

class Equipment(Component):
    instances = set()
    __slots__ = ['unit', 'left_hand', 'right_hand', 'body']
    def __init__(self, left=None, right=None, body=None):
        for a, v in zip(self.__slots__[1:], [left, right, body]):
            setattr(self, a, v if v else None)

    def equip(entity, item, part):
        if getattr(entity.equipment, part):
            return False
        setattr(entity.equipment, part)
        entity.attribute.modify(stats=entity.equipment.part.modifiers)
        return True

    def unequip(self, item, part):
        item = getattr(entity.equipment, part)
        if not item:
            return False
        setattr(entity.equipment, part, None)
        entity.attribute.modify(stats=entity.equipment.part.modifiers, remove=True)
        return True

class Attribute(Component):
    instances = set()
    __slots__ = [
        'unit', 'strength', 'agility', 'intelligence', 'health', 'mana',
        'armor', 'modifiers', 'attrscore'
    ]
    def __init__(self, strength=0, agility=0, intelligence=0):
        self.strength = roll(strength)
        self.agility = roll(agility)
        self.intelligence = roll(intelligence)

        self.modifiers = {key: 0 for key in self.__slots__
                              if key not in ("unit", "modifiers", "attrscore")}
        self.stats()

    def __str__(self):
        attributes = "strength agility intelligence".split()
        attributes = " ".join(
                f"{getattr(self, a)}{check(self.modifiers[a])} ({self.attrscore[a]})" 
                                for a in attributes)
        return super().__str__() + f"s: {attributes}"

    def __call__(self):
        return (self.strength, self.agility, self.intelligence, 
            self.modifiers, self.attrscore)

    def stats(self):
        self.health = Health(self.strength + self.modifiers['strength'])
        self.mana = Mana(self.intelligence + self.modifiers['intelligence'])
        self.armor = Armor(self.agility + self.modifiers['agility'])

        self.attrscore = {key: (getattr(self, key) + self.modifiers[key]) // 2 - 5 
                            for key in "strength agility intelligence".split()}

    def update(self):
        self.health.update()
        self.mana.update()
    
    def modify(self, stat=None, stats=None, remove=False):
        if not stat and not stats:
            raise ValueError("Need a stat to modify")
        if stat and stats:
            raise ValueError("Cannot supply both arguments in modify")
        if stat:
            stats = [stat]
        for stat, value in stats:
            if remove:
                self.modifiers[stat] -= value
            else:
                self.modifiers[stat] += value
        self.stats()

class Health(Component):
    instances = set()
    __slots__ = ['max_hp', 'cur_hp', 'regen', 'regen_counter']
    def __init__(self, strength=0):
        self.max_hp = self.cur_hp = strength * 2

        # let's calculate regen like money. 
        # Precision 2 and store the value before adding to health
        self.regen = int((strength / 50) * 100)
        self.regen_counter = 0
        print("Regen", self.regen)

    def __str__(self):
        return super().__str__() + f"({int(self.cur_hp)}/{int(self.max_hp)})"

    def __call__(self):
        return int(self.cur_hp), int(self.max_hp)

    def update(self):
        hp_gain = (self.regen_counter + self.regen)
        print('hp', hp_gain, hp_gain // 100)
        self.regen_counter = hp_gain % 100
        print('remainder', self.regen_counter)
        self.cur_hp = min(self.cur_hp + hp_gain // 100, self.max_hp)

    def take_damage(self, damage):
        if damage < 0:
            raise Exception("Damage value cannot be negative")
        self.cur_hp += -damage

    @property
    def alive(self):
        return self.cur_hp > 0

class Experience(Component):
    instances = set()
    __slots__ = ['cur_exp', 'cur_lvl', 'next_exp']
    def __init__(self, level=1):
        self.level = level
        self.cur_exp = 0
    def update(self, exp):
        self.cur_exp += exp
        if self.cur_exp >= self.exp_needed:
            self.level += 1
            self.cur_exp %= self.next_exp
    @property
    def exp_needed(self):
        return self.level ** 2 * 30

class Mana(Component):
    instances = set()
    __slots__ = ['max_mp', 'cur_mp']
    def __init__(self, intelligence=0):
        self.max_mp = self.cur_mp = intelligence * 1.5
        self.regen = intelligence / 6
    def __str__(self):
        return super().__str__() + f"({int(self.cur_mp)}/{int(self.max_mp)}"
    def __call__(self):
        return int(self.cur_mp), int(self.max_mp)
    def update(self):
        self.cur_mp = min(self.cur_mp + self.regen, self.max_mp)

class Armor(Component):
    instances = set()
    __slots__ = ['armor']
    def __init__(self, agility=0):
        self.armor= agility * .25 + 3

class Damage(Component):
    instances = set()
    __slots__ = ['unit', "damages"]
    PHYSICAL, MAGICAL = range(2)
    # piercing/bludgeoning/slashing/bleeding/radiating
    def __init__(self, damage=None, damages=None):
        self.damages = {}
        if not damage and not damages:
            raise ValueError('Need to add a damage/damage type for init')
        if damage:
            damages = [damage]
        for dmg, dtype in damages:
            if isinstance(dmg, str):
                dmg = Die.construct(dmg)
            if dtype in self.damages.keys():
                self.damages[dtype].append(dmg)
            else:
                self.damages[dtype] = [dmg]

    def __call__(self):
        damage_per_type = []
        for dtype, damages in self.damages.items():
            total_damage = 0
            for dmg in damages:
                if isinstance(dmg, Die):
                    dmg = next(dmg.roll())
                total_damage += dmg
            damage_per_type.append((dtype, total_damage))
        return damage_per_type

    @property
    def info(self):
        damage_info = []
        for dtype, damages in self.damages.items():
            for dmg in damages:
                if isinstance(dmg, Die):
                    dmg = dmg.ranges
                damage_info.append(str(dmg))
        if len(damage_info):
            return str(damage_info.pop())
        return "/".join([str(d) for d in damage_info])
        
# class Health(Component):
#     __slots__ = ['unit', 'max_hp', 'cur_hp']
#     def __init__(self, health=0):
#         self.max_hp = self.cur_hp = health

#     @property
#     def alive(self):
#         return self.cur_hp > 0

    #     def update(self):
    #         if self.unit.has_component('attribute'):
    #             strength = self.unit.get_component('attribute').strength
    #             self.max_hp = strength * 2 + self.max_hp
    #             self.cur_hp = strength * 2 + self.cur_hp

    #     def take_damage(self, damages):
    #         for dtype, damage in damages:
    #             print(f"{self.unit} was hit with {damage} damage.")
    #             if self.unit.has('defense'):
    #                 blocked = damage
    #                 damage = self.unit.get('defense').calculate((dtype, damage))
    #                 print(f"{self.unit} blocked {blocked - damage} damage.")
    #             else:
    #                 print(f"{self.unit} has no defense and takes full damage.")            
    #             self.cur_hp -= damage
    #             print(f"{self.unit} took {damage} damage. " +
    #                   f"{self.unit} has {self.cur_hp} health left.")

    # class Defense(Component):
    #     __slots__ = ['unit', "armor", "resistance"]
    #     FLAG = 1 << Component.bitflag
    #     Component.bitflag += 1
    #     def __init__(self, armor=0, resistance=0):
    #         self.armor = armor
    #         self.resistance = resistance

    #     def calculate(self, damage=None, damages=None):
    #         print(f"{self.unit} has {self.armor} armor and {self.resistance} resistance.")
    #         if not damage and not damages:
    #             raise ValueError('Need to add a damage/damage type for init')
    #         total_damage = []
    #         if damage:
    #             damages = [damage,]
    #         for dtype, damage in damages:
    #             if dtype == 1:
    #                 total_damage.append(damage - self.armor)
    #             else:
    #                 total_damage.append(damage * self.resistance)
    #         return sum(total_damage)

# class Mana(Component):
#     __slots__ = ['unit', 'max_mp', 'cur_mp']
#     def __init__(self, mana=0):
#         self.max_mp = self.cur_mp = mana

    #     def update(self):
    #         if self.unit.has_component('attribute'):
    #             intelligence = self.unit.get_component('attribute').intelligence
    #             self.max_mp = intelligence * 2 + self.max_mp
    #             self.cur_mp = intelligence * 2 + self.cur_mp

    # class Energy(Component):
    #     __slots__ = ['unit']
    #     FLAG = 1 << Component.bitflag
    #     Component.bitflag += 1
print([sc.classname() for sc in Component.__subclasses__()])
print(all([(sc.classname(), hasattr(sc, 'instances')) for sc in Component.__subclasses__()]))
# COMPONENTS = {
#     subclass.__name__.lower(): {} for subclass in Component.__subclasses__()
# }
# BITS = {
#     subclass.__name__.lower(): 1 << bit
#         for bit, subclass in enumerate(Component.__subclasses__())
# }
# print(COMPONENTS)
# print(BITS)
# Component.set_flags()

if __name__ == "__main__":
    from doctest import testmod
    import json

    testmod()
    component_dictionary = {
        subclass.__name__.lower(): [v for v in subclass.__slots__ if v != 'unit']
        for subclass in Component.__subclasses__()
    }
    print(json.dumps(component_dictionary, sort_keys=True, indent=4, separators=(',', ':')))