# components.py
from collections import namedtuple, Iterable
from .ecs import Component
from .die import Die
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
    def __init__(self, name, attr):
        self.unit = unit
        self.intelligence = intelligence

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
    __slots__ = ['unit', 'level']
    def __init__(self, level):
        '''Binds unit to this class
        >>> unit = namedtuple("Unit", "max_hp level")
        >>> e = Experience(unit(16, 2))
        '''
        self.level = level

    def calculate(self):
        if not self.unit.has('health'):
            raise ValueError('Experience cannot be calculated without health')

        if self.level == 1:
            exp = self.unit.get('health').max_hp // 8
        else:
            exp = self.unit.get('health').max_hp // 6

        if self.level > 9:
            exp *= 20
        elif self.level > 6:
            exp *= 4

        return exp

'''
Strength, measuring physical power
Dexterity, measuring agility
Constitution, measuring endurance
Intelligence, measuring reasoning and memory
Wisdom, measuring perception and insight
Charisma, measuring force of personality
'''

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
