# Some formulas to use when developing a character
from collections import namedtuple

STATS = namedtuple("STATS", "str con int wis agi lck")
MALE = STATS(1, 0, 0, 0, 0, 0)
FEMALE = STATS(0, 0, 0, 0, 1, 0)

HUMAN = STATS(3, 3, 3, 3, 3, 3)
ELVEN = STATS(2, 2, 4, 3, 4, 3)
ORCEN = STATS(4, 5, 2, 2, 3, 2)
DWARF = STATS(3, 4, 2, 3, 3, 3)

SQUIRE = STATS(2, 2, 0, 0, 1, 0)
ARCHER = STATS(0, 1, 0, 0, 3, 1)
WIZARD = STATS(0, 0, 2, 3, 0, 0)

print("RACE: ", sum(HUMAN), sum(ELVEN), sum(ORCEN), sum(DWARF))
print("CLASS: ", sum(SQUIRE), sum(ARCHER), sum(WIZARD))
print("RACE + SEX: ", sum(x+y for x, y in zip(HUMAN, MALE)), sum(x+y for x, y in zip(HUMAN, FEMALE)))
