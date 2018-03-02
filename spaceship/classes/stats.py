# stats.py
from collections import namedtuple
from component import Component
from die import Die
import random
import re

class Stats(Component):
    '''Stats componenet used in unit classes'''
    __slots__ = ['str', 'con', 'agi', 'int', 'wis', 'luc']
    def __init__(self, stats):
        '''Creates a valid stats object using a die string or container of 
        integers or die strings as stat parameters instead of normal integer 
        values. These stat values will be binded to the stats in the given
        order.

        >>> s = Stats((1, 2, 3, 4, 5, 6))
        >>> s
        STATS: (STR: 1, CON: 2, AGI: 3, INT: 4, WIS: 5, LUC: 6)
        >>> s = Stats("1d6 1d6 1d6 1d6 1d6 1d6")
        >>> s = Stats("1d6 1d6 1d6 1d6 1d6 1d6".split())
        >>> from entity import Entity
        >>> e = Entity('hero')
        >>> e.component = s
        >>> list(type(e).__name__ for e in e.components)
        ['Stats']
        '''
        string_single = isinstance(stats, str)
        if string_single:
            stats = stats.split()
        
        if string_single or all([isinstance(s, str) for s in stats]):
            stats = [next(Die.construct(stat).roll()) for stat in stats]

        for attr, stat in zip(self.__slots__, stats):
            setattr(self, attr, stat)

    def __repr__(self):
        '''Returns stat information for dev'''
        return f'{self.__class__.__name__.upper()}: ({self})'

    def __str__(self):
        '''Returns stat information for user'''
        return ", ".join(f'{s.upper()}: {getattr(self, s)}' 
                           for s in self.__slots__)

if __name__ == "__main__":
    from doctest import testmod
    testmod()