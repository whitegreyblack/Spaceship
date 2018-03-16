# die.py
from collections import namedtuple
import random
import re

class Die:
    '''Die class used in determining a controlled random number. Can be
    used with any attribute, chance mechanic or random event occurance.
    Examples include weapon damage, drop rate, enemy spawning.

    >>> between = lambda x, a, b: a<=x<=b
    >>> ex_str = "2d8+3"
    >>> Die.eval_dice_string(ex_str)
    die_params(sides=8, mult=2, sub=3)
    >>> d = Die()
    >>> d
    Die(sides=6, mult=1, mod=0): 1d6
    >>> between(next(d.roll()), *d.ranges())
    True
    >>> Die(multiplier=2)
    Die(sides=6, mult=2, mod=0): 2d6
    >>> Die(multiplier=2, modifier=2)
    Die(sides=6, mult=2, mod=2): 2d6+2
    >>> Die.construct("2d6+2")
    Die(sides=6, mult=2, mod=2): 2d6+2
    '''
    __slots__ = ['multiplier', 'sides', 'modifier']
    def __init__(self, sides=6, multiplier=1, modifier=0):
        '''Checks all three parameters for correct values. If incorrect
        values are found then init raises ValueErrors and class creation
        is aborted.
        '''
        if sides < 2:
            raise ValueError('Number of sides on die must be 2 or more')

        if multiplier < 0:
            raise ValueError('Die multiplier cannot be zero')

        if not isinstance(modifier, int):
            raise ValueError('Die modifier must be an integer value')

        self.sides = sides
        self.multiplier = multiplier
        self.modifier = modifier

    @staticmethod
    def eval_dice_string(string):
        '''Used to recognize valid dice strings. Matches input string with
        regex used in determining dice strings. If match found then converts
        die string into three integer parameters used in initializing dices.
        '''
        dice_init = namedtuple("die_params", "sides, mult, sub")
        die_regex = r"\d{1,3}d\d{1,3}(?:(?:\+|\-)\d{1,4}){0,1}"
        if bool(re.match(die_regex, string)):
            try:
                string, sub = re.split(r'(?:\+|\-)', string)
            except ValueError:
                sub = 0
            mult, sides = string.split('d')
            return dice_init(int(sides), int(mult), int(sub))
        raise ValueError('Die string is invalid')

    @staticmethod
    def split_dice_string(string: object) -> str:
        '''Used to recognize args made up of multiple valid die strings.
        Returns a list of deliminated die strings used in iterating
        '''
        single_die = isinstance(string, str)
        if single_die:
            string = string.split()
        
        if single_die or all([isinstance(s, str) for s in string]):
            string = [next(Die.construct(stat).roll()) for stat in string]
        return string


    @classmethod
    def construct(cls, string):
        '''Creates a valid Die object using a die string instead of
        normal parameters
        '''
        return cls(*Die.eval_dice_string(string))

    def check_sign(self, value):
        '''Converts all values into string representations. If value is 
        positive, a plus sign is added to the string. If value is zero,
        then function returns an empty string
        '''
        string = ""
        if value < 0:
            string = str(value)
        elif value > 0:
            string = f"+{value}"
        return string
    
    def roll(self):
        '''Returns a random value found in between the range roll'''
        yield random.randint(*self.ranges)

    @property
    def ranges(self):
        '''Returns the range of the rolls possible by the die'''
        lower = self.multiplier + self.modifier
        higher = self.multiplier * self.sides + self.modifier
        return lower, higher

    @property
    def average(self, times, integer=True):
        '''Returns the sum of rolls divided number or times rolled'''
        total = sum(next(self.roll()) for _ in range(times))
        return total // times if integer else total / times

    def __repr__(self):
        '''Returns die info for developer'''
        # c=self.__class__.__name__
        # s=self.sides
        # mu=self.multiplier
        # mo=self.modifier
        # return f"{c}(sides={s}, mult={mu}, mod={mo})"
        return f"{self.__class__.__name__}({self})"

    def __str__(self):
        '''Returns die info for end-user'''
        return f"{self.multiplier}d{self.sides}{self.check_sign(self.modifier)}"

if __name__ == "__main__":
    from doctest import testmod
    testmod()