from collections import namedtuple
from die import Die
import random
import re

class Stats:
    '''Stats componenet used in unit classes'''
    def __init__(self, values):
        self.str, self.con, self.agi, self.int, self.wis, self.luc = values

    @classmethod
    def construct(cls, strings):
        '''Creates a valid stats object using a die string as
        stat parameters instead of normal integer values
        '''
        if isinstance(strings, str):
            strings = strings.split() 
        return cls(next(Die.construct(s).roll()) for s in strings)

    def __repr__(self):
        '''Returns stat information for dev'''
        return f'{self.__class__.__name__.upper()}: ({self})'

    def __str__(self):
        '''Returns stat information for user'''
        return \
            f"STR: {self.str}, CON: {self.con}, AGI: {self.agi}, INT: {self.int}, WIS: {self.wis}, LUC: {self.luc}"

if __name__ == "__main__":
    s = Stats((1, 1, 1, 1, 1, 1))
    print(s)

    s = Stats.construct(("1d6", "1d6", "1d6", "1d6", "1d6", "1d6"))
    print(s)

    s = Stats.construct(("1d6 1d6 1d6 1d6 1d6 1d6"))
    print(s)

    s = Stats.construct(("1d6+3", "1d6", "1d6", "1d6", "1d6", "1d6"))
    print(s)
    print(repr(s))