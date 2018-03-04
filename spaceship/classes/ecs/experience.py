# experience.py
from collections import namedtuple

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

if __name__ == "__main__":
    unit = namedtuple("Unit", "max_hp level")

    e = Experience(unit(16, 2))
    print(e.calculate())

    print(experience_unit(unit(16, 2)))
    print(experience(16, 2))
