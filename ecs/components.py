# components.py
from collections import namedtuple, Iterable
from ecs import Component
from die import Die
import random
import re
'''
Entities: name, id
    Tile: render, position
        Floor, Wall, Door
    Unit: render, position, mover, health
        Hero, Enemy
    Item: render, damage, armor
        Sword, Wand

Component List:
    Stats: [s | c | a | i | w | l]
    Mover
    Damage:
        Type (physical, magical, pure)
        Range
    Energy:
        Total
        Current
        Refresh
    Health:
        Total
        Current
        Refresh
    Mana:
        Total
        Current
        Refresh
'''
class Render(Component):
    __slots__ = ['unit', 'symbol', 'foreground', 'background']
    def __init__(self, unit, symbol, foreground="#ffffff", background="#000000"):
        '''Render component that holds all information that allows the map
        to be drawn with correct characters and colors
        >>> r = Render(None, '@')
        >>> r
        Render(symbol=@, foreground=#ffffff, background=#000000)
        >>> r.symbol == '@'
        True
        '''
        self.unit = unit
        self.symbol = symbol
        self.foreground = foreground
        self.background = background

class Description(Component):
    __slots__ = ['unit', 'name', 'less', 'more']
    def __init__(self, unit, name, less=None, more=None):
        self.unit = unit
        self.name = name
        self.less = less
        self.more = more

class Damage(Component):
    __slots__ = ['unit', "damage",]
    def __init__(self, unit, damage):
        self.unit = unit
        self.damage = Die.construct(damage)

class Defense(Component):
    __slots__ = ['unit', "armor",]
    def __init__(self, unit, armor):
        self.unit = unit
        self.armor = armor

class Attribute(Component):
    __slots__ = ['unit', 'strength', 'agility', 'intelligence']
    def __init__(self, unit, strength, agility, intelligence):
        '''
        >>> Attribute(None, 5, 5, 5)
        Attribute(strength=5, agility=5, intelligence=5)
        '''
        self.unit = unit
        self.strength = strength
        self.agility = agility
        self.intelligence = intelligence

class Strength(Component):
    def __init__(self, unit, strength):
        self.unit = unit
        self.strength = strength
        self.health = strength * 2

class Agility(Component):
    def __init__(self, unit, agility):
        self.unit = unit
        self.agility = agility

class Intelligence(Component):
    __slots__ = ["intelligence", "mana"]
    def __init__(self, name, attr):
        self.unit = unit
        self.intelligence = intelligence

class Health(Component):
    def __init__(self):
        self.max_hp = self.cur_hp = 0
    
    def __str__(self):
        return f"Health: {self.cur_hp}/{self.max_hp}"

    # def status_bonuses(self, strbon, conbon):
    #     self.mod_hp = strbon + conbon * 2
    #     self.max_hp = self.cur_hp = self.hp + self.mod_hp

    # def take_damage(self, heal):
    #     self.hitpoints += damage

    # def heal_damage(self, heal):
    #     self.hitpoints += heal

    # class Mana(Component):
    #     mp = 5
    #     def __init__(self):
    #         self.max_mp = self.cur_mp = 0
        
    #     def __str__(self):
    #         return f"Mana: {self.cur_mp}/{self.max_mp}"

    #     def status_bonuses(self, intbon, wisbon):
    #         self.mod_mp = intbon + wisbon * 2
    #         self.max_mp = self.cur_mp = self.mp + self.mod_mp

    #     def use_points(self, usage):
    #         self.cur_mp -= usage
        
    #     def gain_points(self, regen):
    #         self.cur_mp += usage
    
def experience(max_hp, level):
    '''Handles calculating level based on unit max level and health'''
    if level == 1:
        exp = max_hp // 8
    else:
        exp = max_hp // 6
    if level > 9:
        exp *= 20
    elif level > 6:
        exp *= 4
    return exp

def experience_unit(unit):
    '''Wrapper function to handle unit parameter'''
    return experience(unit.max_hp, unit.level)

class Experience:
    '''Experience class to hold experience calculate function'''
    __slots__ = ['unit']
    def __init__(self, unit):
        '''Binds unit to this class
        >>> unit = namedtuple("Unit", "max_hp level")
        >>> e = Experience(unit(16, 2))
        '''

        self.unit = unit

    def calculate(self):
        if self.unit.level == 1:
            exp = self.unit.max_hp // 8
        else:
            exp = self.unit.max_hp // 6
        if self.unit.level > 9:
            exp *= 20
        elif self.unit.level > 6:
            exp *= 4
        return exp

class Stats(Component):
    '''Stats componenet used in unit classes. Creates a valid stats object 
        using a die string or container of integers or die strings as stat 
        parameters instead of normal integer values. These stat values will 
        be binded to the stats in the given order.
        >>> s = Stats(unit(5, 1), (1, 2, 3, 4, 5, 6))
        >>> s
        Stats(unit=Unit(max_hp=5, level=1), str=1, con=2, agi=3, int=4, wis=5, luc=6)
        >>> s = Stats(unit(5, 1), "1d6 1d6 1d6 1d6 1d6 1d6")
        >>> s = Stats(unit(5, 1), "1d6 1d6 1d6 1d6 1d6 1d6".split())
        '''
    __slots__ = ['unit', 'str', 'con', 'agi', 'int', 'wis', 'luc']
    def __init__(self, unit, stats):

        self.unit = unit
        if not isinstance(stats, (str, Iterable)):
            raise ValueError('Invalid arguments')

        # helper function from Die
        stats = Die.split_dice_string(stats)
        for attr, stat in zip(self.__slots__[1:], stats):
            setattr(self, attr, stat)

    def __repr__(self):
        '''Returns stat information for dev'''
        return f'{self.__class__.__name__}({self})'

    def __str__(self):
        '''Returns stat information for user'''
        return ", ".join(f'{s}={getattr(self, s)}' for s in self.__slots__)

if __name__ == "__main__":
    from doctest import testmod
    unit = namedtuple("Unit", "max_hp level")
    testmod()
