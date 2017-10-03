# Some formulas to use when developing a character
from collections import namedtuple

STATS = namedtuple("STATS", "str con dex int wis cha")
MALE = STATS(1, 0, 0, 0, 0, 0)
FEMALE = STATS(0, 0, 0, 0, 1, 0)

HUMAN = STATS(3, 3, 3, 3, 3, 3)
HUMAN_BONUS = STATS(0, 0, 0, 0, 0, 0)
ELVEN = STATS(2, 2, 4, 4, 4, 2)
ELVEN_BONUS = STATS(-1, -1, 1, 1, 1, -1)
ORCEN = STATS(5, 5, 2, 1, 3, 2)
ORCEN_BONUS = STATS(2, 2, -1, -2, 0, -1)
DWARF = STATS(4, 4, 2, 3, 2, 3)
DWARF_BONUS = STATS(1, 1, -1, 0, -1, 0)
BEAST = STATS(4, 3, 4, 3, 2, 2)
BEAST_BONUS = STATS(0, 1, -1, 0, 1, -1)
SQUIRE = STATS(2, 2, 1, 0, 0, 0)
ARCHER = STATS(0, 1, 3, 0, 0, 1)
WIZARD = STATS(0, 0, 0, 2, 3, 0)
DRUIDS = STATS(1, 0, 0, 2, 2, 0)
CLERIC = STATS(0, 1, 0, 2, 2, 0)

EXTRA = 3

# print("RACE: ", sum(HUMAN), sum(ELVEN), sum(ORCEN), sum(DWARF), sum(BEAST))
# print("CLASS: ", sum(SQUIRE), sum(ARCHER), sum(WIZARD))
# print("RACE + SEX: ", sum(x+y for x, y in zip(HUMAN, MALE)), sum(x+y for x, y in zip(HUMAN, FEMALE)))
