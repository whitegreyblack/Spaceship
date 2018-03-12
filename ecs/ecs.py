# component.py
from bearlibterminal import terminal as term
import random
from .die import Die

class System:
    def update(self):
        raise NotImplementedError

class Component:
    # bitflag = 0
    # __instances = {}
    def __repr__(self):
        '''Returns stat information for dev'''
        return f'{self.__class__.__name__}({self})'

    def __str__(self):
        '''Returns stat information for user'''
        return ", ".join(f'{s}={getattr(self, s)}' 
            for s in self.__slots__
            if bool(hasattr(self, s) and getattr(self, s)))

    # Reference link to currently connected entity unit
    # @property
    # def unit(self):
    #     return self._unit

    @classmethod
    def name(cls):
        return cls.__name__.lower()

    # @unit.setter
    # def unit(self, unit):
    #     self._unit = unit
    #     if self.name not in Component.__instances:
    #         Component.__instances[subclass] = {unit.eid: self}
    #     else:
    #         Component.__instances[subclass].update({unit.eid: self})

    # @staticmethod
    # def get(key):
    #     return Component.__instances[key]

class Render(Component):
    __slots__ = ['_unit', 'symbol', 'foreground', 'background']
    # FLAG = 1 << Component.bitflag
    # Component.bitflag += 1
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

    @property
    def render(self):
        return self.background, f"[c={self.foreground}]{self.symbol}[/c]"

class Position(Component):
    __slots__ = ['unit', 'x', 'y']
    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y

    @property
    def position(self):
        return self.x, self.y

class Backpack(Component):
    __slots__ = ['unit', 'backpack']
    def __init__(self, backpack=[None for _ in range(6)]):
        self.max = 6
        self.backpack = backpack

class Equipment(Component):
    __slots__ = ['unit', 'left_hand', 'right_hand', 'body']
    def __init__(self, lh=None, rh=None, body=None):
        if lh:
            self.left_hand = lh
        if rh:
            self.right_hand = rg
        if body:
            self.body = body

    # -- Needs Validation --
    # class Description(Component):
    #     __slots__ = ['unit', 'name', 'less', 'more']
    #     FLAG = 1 << Component.bitflag
    #     Component.bitflag += 1
    #     def __init__(self, name, less=None, more=None):
    #         self.name = name
    #         self.less = less
    #         self.more = more
            
    # class Attribute(Component):
    #     __slots__ = ['unit', 'strength', 'agility', 'intelligence']
    #     FLAG = 1 << Component.bitflag
    #     Component.bitflag += 1
    #     def __init__(self, strength, agility, intelligence):
    #         '''
    #         >>> Attribute(5, 5, 5)
    #         Attribute(strength=5, agility=5, intelligence=5)
    #         '''
    #         self.strength = strength
    #         self.agility = agility
    #         self.intelligence = intelligence

    #     def update(self):
    #         for attr in 'health mana defense'.split():
    #             if self.unit.has(attr):
    #                 self.unit.get(attr).update()

class Damage(Component):
    __slots__ = ['unit', "damages"]
    # FLAG = 1 << Component.bitflag
    # Component.bitflag += 1
    MAGICAL, PHYSICAL = range(2)
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

    @property
    def deal(self):
        damage_per_type = []
        for dtype, damages in self.damages.items():
            total_damage = 0
            for dmg in damages:
                if isinstance(dmg, Die):
                    dmg = next(dmg.roll())
                total_damage += dmg
            damage_per_type.append((dtype, total_damage))
        return damage_per_type

    # class Health(Component):
    #     __slots__ = ['unit', 'max_hp', 'cur_hp']
    #     FLAG = 1 << Component.bitflag
    #     Component.bitflag += 1
    #     def __init__(self, health=0):
    #         self.max_hp = self.cur_hp = health

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
    #     FLAG = 1 << Component.bitflag
    #     Component.bitflag += 1
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
print([sc.name() for sc in Component.__subclasses__()])

class Entity:
    '''
    Basic container for entity objects. Holds a list of components which is used
    to represent certain objects in game world.

    # >>> e = Entity(components=[Description('hero'),])
    # >>> e, Entity.compdict
    # (hero, {'description': {0: Description(unit=hero, name=hero)}})
    # >>> e.has_component('description')
    # True
    # >>> e.get_component('description')
    # Description(unit=hero, name=hero)
    # >>> e.del_component('description')
    # >>> e.has_component('description')
    # False
    # >>> list(e.components)
    # []
    >>> e=Entity(components=[
    ...     Render('@'),
    ... ])
    >>> e.render
    Render(symbol=@, foreground=#ffffff, background=#000000)
    '''
    __slots__ = ['eid', 'delete', 'ai', 'moveable', 'race'] + [
        sc.name() for sc in Component.__subclasses__()
    ]
    EID = 0
    # instances = {}
    # compdict = {c.__name__.lower(): {} for c in Component.__subclasses__()}
    def __init__(self, components=None):
        self.eid = Entity.EID
        Entity.EID += 1
        # self.FLAG = 0
        if components:
            for component in components:
                if isinstance(component, Component):
                    setattr(self, component.name(), component)
                else:
                    setattr(self, *component)

    def __str__(self):
        # description = self.get_component('description')
        if hasattr(self, 'description') and description.name:
            return description.name
        return str(self.eid)

    def __repr__(self):
        return f"Entity(eid={self})"

    def __hash__(self):
        return self.eid

    def __eq__(self, other):
        return self.eid == hash(other.eid)
    
    def __lt__(self, other):
        return self.eid < hash(other.eid)
    # # ? should I move these into components?
    @property
    def components(self):
        for component in self.__slots__:
            if hasattr(self, component) and getattr(self, component) is not None:
                yield repr(getattr(self, component))

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

COMPONENTS = {
    subclass.__name__.lower(): {} for subclass in Component.__subclasses__()
}
BITS = {
    subclass.__name__.lower(): 1 << bit
        for bit, subclass in enumerate(Component.__subclasses__())
}
# print(COMPONENTS)
# print(BITS)
# Component.set_flags()

if __name__ == "__main__":
    from doctest import testmod
    testmod()