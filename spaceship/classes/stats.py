from collections import namedtuple
from die import Die
import random
import re

class Example:
    def __init__(self, stats):
        self.stats = Stats(stats)

class Stats:
    '''Stats componenet used in unit classes'''
    __slots__ = ['str', 'con', 'agi', 'int', 'wis', 'luc']
    def __init__(self, stats):
        string_single = isinstance(stats, str)
        if string_single:
            stats = stats.split()

        string_multiple = all([isinstance(s, str) for s in stats])
        if string_single or string_multiple:
            stats = [next(Die.construct(stat).roll()) for stat in stats]

        for attr, stat in zip(self.__slots__, stats):
            setattr(self, attr, stat)

    # @classmethod
    # def construct(cls, strings):
    #     '''Creates a valid stats object using a die string as
    #     stat parameters instead of normal integer values
    #     '''
    #     if isinstance(strings, str):
    #         strings = strings.split() 
    #     return cls(next(Die.construct(s).roll()) for s in strings)

    def __repr__(self):
        '''Returns stat information for dev'''
        return f'{self.__class__.__name__.upper()}: ({self})'

    def __str__(self):
        '''Returns stat information for user'''
        return ", ".join(f'{s.upper()}: {getattr(self, s)}' for s in self.__slots__)

if __name__ == "__main__":
    s = Stats((1, 2, 3, 4, 5, 6))
    print(s)

    s = Stats("1d6 1d6 1d6 1d6 1d6 1d6")
    print(s)

    s = Stats("1d6 1d6 1d6 1d6 1d6 1d6".split())
    print(s)

    e = Example("1d6 1d6 1d6 1d6 1d6 1d6")
    classes = [e]
    for c in classes:
        if hasattr(c, 'stats') and isinstance(c.stats, Stats):
            print(e.stats)