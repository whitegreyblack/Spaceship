from collections import namedtuple
'''
# CC_STRINGS.PY
# Holds the multiline columns used in create character
# Placed here since keeping them in cc is messy
'''[1:]

_world = "Calabaston"

_col1 = """
Gender  : {:>10}
Race    : {:>10}
Capital : {:>10}
Class   : {:>10}

Gold    : {:>10}
Level   : {:>10}
Adv Exp : {:>10}

HP      : [c=#00ffff]{:>10}[/c]
MP      : [c=#00ffff]{:>10}[/c]
SD      : [c=#00ffff]{:>10}[/c]
"""[1:]

_col2 = """
SKILLS  : \n  {}\n  {}

   TOTAL  GB  RB  CB
STR : [c=#00ffff]{:>2}[/c]
CON : [c=#00ffff]{:>2}[/c]
DEX : [c=#00ffff]{:>2}[/c]
INT : [c=#00ffff]{:>2}[/c]
WIS : [c=#00ffff]{:>2}[/c]
CHA : [c=#00ffff]{:>2}[/c]
"""[1:]

_bon = """{:>2}\n{:>2}\n{:>2}\n{:>2}\n{:>2}\n{:>2}"""

_col3 = """
HEAD  : {:<5}\nNECK  : {:<5}\nBODY  : {:<5}
ARMS  : {:<5}\nHANDS : {:<5}\nLHAND : {:<5}
RHAND : {:<5}\nRING1 : {:<5}\nRING2 : {:<5}
WAIST : {:<5}\nLEGS  : {:<5}\nFEET  : {:<5}
"""[1:]

# Some formulas to use when developing a character
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
