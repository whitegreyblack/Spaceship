from collections import namedtuple
import random
import re

class Die:
    __slots__ = ['multiplier', 'sides', 'modifier']
    def __init__(self, sides=6, multiplier=1, modifier=0):
        if sides < 2:
            raise ValueError('Number of sides on die must be 2 or more')

        if multiplier < 0:
            raise ValueError('Die multiplier cannot be zero')

        if not isinstance(modifier, int):
            raise ValueError('Die modifier must be an integer value')

        self.sides = sides
        self.multiplier = multiplier
        self.modifier = modifier

    @property
    def string(self):
        return self.__str__()

    @classmethod
    def parse(cls, string):
        '''Creates a valid Die object using a die string instead of
        normal parameters
        '''
        return cls(*Die.eval_dice_string(string))

    @staticmethod
    def eval_dice_string(string):
        '''Used to recognize valid dice strings. Matches input string with
        regex used in determining dice strings
        '''
        dice_init = namedtuple("die_params", "sides, mult, sub")
        die_regex = r"\d{1,3}d\d{1,3}(?:\+|\-)\d{1,4}"
        if bool(re.match(die_regex, string)):
            try:
                string, sub = re.split(r'(?:\+|\-)', string)
            except ValueError:
                sub = 0
            mult, sides = string.split('d')
            return dice_init(sides, mult, sub)
        raise ValueError('Die string is invalid')

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
        # return value if value < 0 else f"+{value}" if value > 0 else ""

    def roll(self):
        value = 0
        for die in range(self.multiplier):
            value += random.randint(1, self.sides)
        yield value

    def ranges(self):
        return 1 + self.modifier, self.multiplier * self.sides + self.modifier

    def __repr__(self):
        c=self.__class__.__name__
        s=self.sides
        mu=self.multiplier
        mo=self.modifier
        return f"{c}(sides={s}, mult={mu}, mod={mo}): {self.string}"

    def __str__(self):
        return f"{self.multiplier}d{self.sides}{self.check_sign(self.modifier)}"

if __name__ == "__main__":
    d = Die()
    print(d.__repr__(), d.ranges(), next(d.roll()))

    d = Die(multiplier=2)
    print(d, d.ranges(), next(d.roll()))

    d = Die(multiplier=2, modifier=2)
    print(d, d.ranges(), next(d.roll()))

    ex_str = "2d8+3"
    print(Die.eval_dice_string(ex_str))

    ex_str = "2d8+3"
    x, y = re.split(r'(?:\+|\-)', ex_str)