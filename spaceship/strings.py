from collections import namedtuple
'''
# CC_STRINGS.PY
# Holds the multiline columns used in create character
# Placed here since keeping them in cc is messy
'''

'''Constants used in main and other modules -- equivalent to globals'''
FONT_PATH = "./spaceship/assets/fonts/"
IMG_PATH = "./spaceship/assets/"
MENU_SCREEN_WIDTH, MENU_SCREEN_HEIGHT = 80, 25
MENU_FONT_WIDTH, MENU_FONT_HEIGHT = 8, 16

GAME_SCREEN_WIDTH, GAME_SCREEN_HEIGHT = 80, 50
GAME_FONT_WIDTH, GAME_FONT_HEIGHT = 8, 8

FOV_RADIUS = 25

# CHARACTER MENU GLOBALS
CM_TITLE = 1
CM_SUBTITLE = 2
CM_BORDER_WIDTH = 80
CM_BORDER_HEIGHT = ()
CM_COLUMN_WIDTH = 12
CM_COLUMN_START = 1, 15, 27
CM_FOOTER_HEIGHT = 22

# OPTION MENU GLOBALS
OPT_TITLE = 1
OPT_BORDER_WIDTH = 80
OPT_BORDER_HEIGHT = (3, 24)

# ITEM CONSTANTS
ITEM_DROP_RATE=0 # drop rate from monsters in dungeons
ITEM_FIND_RATE=0 # chances item spawns in dungeon
ITEM_PREREVEAL=0 # basically pre identification rate 

# ROOM CONSTANTS
ROOM_MIN_PLACE=0
ROOM_MAX_PLACE=0
ROOM_HALL_SIZE=2
ROOM_DOOR_RATE=0

GAME_TITLE_VERSION="v 0.0.4"
GAME_TITLE_WIDTH=46
GAME_TITLE_HEIGHT=6
GAME_TITLE=''' \
 ___                           _     _       
/  _\_ __   __ _  ___ ___  ___| |__ (_)_ __  
\  \| '_ \ / _` |/ __/ _ \/ __| '_ \| | '_ \ 
_\  \ |_) | (_| | (_|  __/\__ \ | | | | |_) |
\___/ .__/ \__,_|\___\___||___/_| |_|_| .__/ 
    |_|                               |_|    
'''[1:]

GAME_TITLE_SHORT ='''
 ██████╗ █████╗ ██████╗  █████╗ ██╗    
██╔════╝██╔══██╗██╔══██╗██╔══██╗██║    
██║     ███████║██████╔╝███████║██║    
██║     ██╔══██║██╔══██╗██╔══██║██║    
╚██████╗██║  ██║██████╔╝██║  ██║██████╗
 ╚═════╝╚═╝  ╚═╝╚═════╝ ╚═╝  ╚═╝╚═════╝
     Act I: Bones of the Ancestors
'''[1:]

#------------------------------------------------------------------------------
# SCENE :- MAKE 
#------------------------------------------------------------------------------
_col1 = """
Gender  : {:>10}{delim}
Race    : {:>10}{delim}
Capital : {:>10}{delim}
Class   : {:>10}{delim}\n
Gold    : {:>10}{delim}
Level   : {:>10}{delim}
Adv Exp : {:>10}{delim}\n
HP      : [c=#00ffff]{:>10}[/c]{delim}
MP      : [c=#00ffff]{:>10}[/c]{delim}
SP      : [c=#00ffff]{:>10}[/c]{delim}
"""[1:]

_col2 = """
SKILLS  : {delim}\n{}{delim}\n{}{delim}{delim}\n

     TOT GB RB CB IB{delim}
STR : [c=#00ffff]{:>2}[/c]{delim}
CON : [c=#00ffff]{:>2}[/c]{delim}
DEX : [c=#00ffff]{:>2}[/c]{delim}
INT : [c=#00ffff]{:>2}[/c]{delim}
WIS : [c=#00ffff]{:>2}[/c]{delim}
CHA : [c=#00ffff]{:>2}[/c]{delim}
"""[1:]

_bon = """
{:>2}{delim}
{:>2}{delim}
{:>2}{delim}
{:>2}{delim}
{:>2}{delim}
{:>2}"""[1:]

_col3 = """
Head  : {:<5}{delim}\nNeck  : {:<5}{delim}\nBody  : {:<5}{delim}
Arms  : {:<5}{delim}\nHands : {:<5}{delim}\nLhand : {:<5}
Rhand : {:<5}{delim}\nRing1 : {:<5}\nRing2 : {:<5}{delim}
Waist : {:<5}{delim}\nLegs  : {:<5}{delim}\nFeet  : {:<5}\n
"""[1:]

bonuses = {
    "STR": "+{} to Strength",
    "CON": "+{} to Constitution",
    "WIS": "+{} to Wisdom",
    "DEX": "+{} to Dexterity",
    "CHA": "+{} to Charisma",
    "WIL": "+{} to Willpower",
    "PER": "+{} to Perception",
    "LUC": "+{} to Luck"
}

# Some formulas to use when developing a character
stats = namedtuple("stats", "str con dex int wis cha")

MALE = stats(1, 0, 0, 0, 0, 0)
FEMALE = stats(0, 0, 0, 0, 1, 0)

HUMAN = stats(3, 3, 3, 3, 3, 3)
HUMAN_BONUS = stats(0, 0, 0, 0, 0, 0)

ELVEN = stats(2, 2, 4, 4, 4, 2)
ELVEN_BONUS = stats(-1, -1, 1, 1, 1, -1)

ORCEN = stats(5, 5, 2, 1, 3, 2)
ORCEN_BONUS = stats(2, 2, -1, -2, 0, -1)

DWARF = stats(4, 4, 2, 3, 2, 3)
DWARF_BONUS = stats(1, 1, -1, 0, -1, 0)

BEAST = stats(4, 3, 4, 3, 2, 2)
BEAST_BONUS = stats(0, 1, -1, 0, 1, -1)

SQUIRE = stats(2, 2, 1, 0, 0, 0)
ARCHER = stats(0, 1, 3, 0, 0, 1)
WIZARD = stats(0, 0, 0, 2, 3, 0)
DRUIDS = stats(1, 0, 0, 2, 2, 0)
CLERIC = stats(0, 1, 0, 2, 2, 0)

EXTRA = 3

start="""
Welcome to the realm of Calabaston. Your spirit has drifited to this place filled with intelligent races, a multitude 
of creatures and monsters, and history colored with tragedy, betrayal, and conquest. If you are willing, come and 
choose the vessel in which you will enter this world. Take careful consideration as your starting point depends on the 
choices you make here. Good luck adventurer.
"""[1:]

race_human="""
The youngest race on the continent of Calabaston, humans were the last to arrive from across the Endless Water, and yet, 
they have thrived and proved to be a dominant force throughout the land. Within less than a hundred years, they have 
built Renmar, the current capital city of the human empire of Rane. Humans can be skilled with a wide array of 
different weaponry and magic and are useful in any class.
"""[1:]

race_dwarf="""
A hardy race, dwarves are most famous for their impenetrable fortresses and mass earthly wealth. Their vast fortune 
allows their people to pursue trades and crafts such as blacksmithing, jewelry, and weaponforging, which would not 
be possible otherwise. Dwarves seen outside of Yugahdah, the dwarven territory, are most often skilled traders, 
merchants, or mercenaries. Dwarves prefer melee weapons but can also use magic and ranged weapons.
"""[1:]

race_beast="""
Beasts have physical differences that set them apart from other races as they are born with a combination of fur, 
scales, horns, and tails. After being driven out of the plains of Tempest, they settled near the north west of the 
wetlands and now call Tiphmore, a gigantic trade city, their new home. Beasts have unusually high health and mana pools 
and are suited for either magic or melee classes.
"""[1:]

race_elven="""
The long-lived, mysterious race of elves reside deep within the forests of Aurendelim. Though they may look frail, 
their appearances betray them as they are more dextereous than other races. They live in accordance to the law of the 
forest and dissaprove of any attempt by other races that try to exploit the forest for its resources. Elven warriors 
are most often seen using magic or ranged weaponry but can be skilled in melee as well.
"""[1:] 

race_orcen="""
Brutish and violent, Orcs are feared by other races, including even beast-folk, due to their warring nature and needs 
to constantly engage in battle. They are split into many different tribal clans throughout the Burning Lands territory 
that struggle to take power among all other factions and claim the Blood-Bone crown, which signifies the strongest orc 
clan. The bone crown is currently located in Lok Gurrah, the largest city in the Burning Lands territory.
"""[1:]

race_ishtahari="""
Among all the races that live across Calabaston, the Ishtahari are the oldest. Yet having lived on the continent 
hundreds of years before any of the other races, they are now as rare to meet as their magic is to learn. They are the 
only race to master two elements of the seven, LIGHT and VOID.
"""[1:]

race_ork="""
"""[1:]

race_goblin="""
"""[1:]

race_troll="""
"""[1:]

knight="""
Warriors of noble heritage, knights make up the elite troops within a military. Their heavy armor and equipment allows 
them to take significant damage without injury and deal high damage in return. They are often seen on the front lines of
armies, being used as vanguards for the army in they serve in. Knights have a high sense of duty and honor to their land
and people
"""[1:]

barbarian="""
Barbarians are fearless warriors on the battlefield. Their tendency to fight with rage and reckless abandon makes even
experienced soldiers hesitant to fight them.
"""[1:]

class_cleric="""
Clerics are holy men who use their magic abilities heal their wounded and injured allies. Their spells are particularly 
effective in eradicating the undead and ghoulish creatures of the night. They prefer using ranged magic but are no
strangers to melee combat.
"""[1:]

class_druid="""
Druids are sages worship the ancient forces of nature which gives them a mystical connection to earth and natural 
abilities. They have a deep relationship with creatures of land and water. Druids are proficient in both physical and 
magical combat as they can use magic to strengthen their phyiscal prowess.
"""[1:]

fighter="""
Fighter is blah blah blah
"""[1:]

paladin="""
Paladin is blah blah blah
"""[1:]

ranger="""
Ranger is blah blah blah
"""[1:]

sorcerer="""
Sorcerer is blah blah blah
"""[1:]

rogue="""
Rogue is blah blah blah
"""[1:]

class_archer="""
Archers are skilled in ranged combat, being able to use an assortment of different ranged weaponry that include bows,
throwing daggers, and javalins. If needed they can use their weapons for melee combat as well. They carry very little, as
their equipment is light and can use sneak and steal abilities on their enemies to stealthily replenish their supplies.
"""[1:]

class_wizard="""
Wizards are students of elemental and arcane magic. Their educational background allows them to read ancient scrolls
as well as use spellbooks. Throught study and memorization they can learn new spells through reading and learning. They
have the largest number of upgradable classes available to them including elementalist, sorcerer, and summoner.
"""[1:]

class_squire="""
Squires are the most basic melee class offered to newly created adventurers. They are the most proficient in melee 
weapons and combat but can be skilled in ranged combat as well. With enough experience and money, squires have to choice
of upgrading their class statuses to the Knight and Paladin class.
"""[1:]

"""
Lancer, 
Archer, Squire, Mystic, Bard, Summoner, Chemist, Dragoon, Geomancer, Monk, Ninja, Samurai, Theif
Scout, Berserker, Pathfinder, Runemaster, Sentinal, Lord, Dragonguard, Explorer, Thunderguard, Guardsman, Shieldmaster
Marksman, sharpshooter, captain, champion, marshal, rider, shaman, enchantress, rider, duelist, fencer, mauler,
pikeman, halberdier, spearman, assassin, trapper, warden, arbiter, enforcer, blademaster, 
"""

subrace_descriptions=[
    [
        "Citizen servents residing in the Rodash Empire", 
        "Travelers who wander the continent of Auriel", 
        "Humans living outside of the borders of the Rodash Empire",
        "Sadukar are those who live in the Icy Gaze north of the Empire",
    ],
    [
        "Family name for mining dwarves from the clan in the Iron Hills",
        "Family name for the royal dwarves from the Triple Shining Mountain",
        "Family name for the military dwarf clan from Stone Keep",
    ],
    [
        "Family name for the elite elven family residing in the Emerald Forest",
        "Local elven family name for the elves residing in the woods of Arundelim",
        "Drow are banished elves residing in the forest hills of the Dark Forest",
    ],
    [
        "Ishma are the titles for light-element users of magic",
        "Ishta are the titles for void-element users of magic",
    ],
    [
        "Mountain orcs reside in the Shadows of Mount Huron",
        "Greenskins reside in swamplands East of Ravenflow",
        "Grayskins are found everywhere on the continent of Auriel",
    ],
    [
        "Goblins live in the caves and hills along the Storm-wrought hills and caves",
        "Hobgoblins are a special type of goblin born among goblins but with more strength",
    ],
    [
        "Cave trolls live among the many shelters provided by the Storm-wrought Ridge",
        "Forest trolls reside in the northern and colder area of the Dark Forest",
        "Ice trolls prefer to live in the coldest areas of the Icy Gaze",
    ]

]

#------------------------------------------------------------------------------
# SCENE :- GAME
#------------------------------------------------------------------------------
status = '''
 {:13}
 {:1}{:1}{:1}

 LVL: {:>6}
 EXP: {:>6}

 HP : {:>6}
 MP : {:>6}

 DMG: {:>6}
 D/M: {:>6}

 STR: [c={}]{:>6}[/c]
 CON: [c={}]{:>6}[/c]
 DEX: [c={}]{:>6}[/c]
 INT: [c={}]{:>6}[/c]
 WIS: [c={}]{:>6}[/c]
 CHA: [c={}]{:>6}[/c]

 GOLD: {:>5}
 TURNS: {:>4}
'''[1:]

profile = [
'''
Name     : {name:>6}
Gender   : {sex:>6}
Race     : {race:>6} 
Class    : {job:>6}

STR      : {:>6}
CON      : {:>6}
DEX      : {:>6}
WIS      : {:>6}
INT      : {:>6}
CHA      : {:>6}
'''[1:],
'''
Damage   : {dmg:>6}
Accuracy : {acc:>5}
'''[1:],
]

dump_template="""
[Character Sheet -- Spaceship]
======== Player Stats ========
Name     : {}
Sex      : {}
Race     : {}
Class    : {}

Level    : {}
Exp      : {}
========   Equipment  ========
He       :
Neck     :
Torso    : Peasant garb
Ring(L)  :
Hand(L)  : Sword
Ring(R)  :
Hand(R)  :
Waist    : Thin rope
Legs     : Common pants
Feet     : Sandals
======== Player Items ========
========  Alignments  ========
========  Relations   ========
"""[1:]

cmd_invalid = "'{}' is not a valid command"
cmd_switch_eq = "Press 'v' to switch to inventory."
cmd_switch_iv = "Press 'q' to switch to equipment."
cmd_unequip_confirm = "Are you sure you want to unequip the {}?"
cmd_unequip = "You unequip the {}."
cmd_equip_none = "No items to equip for that slot."
cmd_equip_two_hand = "You cannot equip a weapon to your {}. \
You are already wielding the {} on your {}."
cmd_equip_query = "Which item to equip?"
cmd_equip = "You equip the {}."
cmd_equip_invalid = "Invalid selection."
cmd_drop_query = "Which item to drop?"
cmd_drop_item = "You drop the {}."
cmd_use_none = "You have no items in your inventory that are usable."
cmd_use_query = "Which item to use?"
cmd_use_item = "You use the {}."
cmd_cannot_use_item = "You cannot use this item."
cmd_eat_query = "Which item to eat?"
cmd_eat_none = "You do not have anything to eat."
cmd_eat_item = "You eat the {}."
cmd_cannot_eat_item = "You cannot eat this item."
cmd_save = "Save and exit game? (Y/N)"
cmd_save_folder = 'saved folder does not exist - creating folder: "./saves"'
cmd_inv_funcs = "What to do with the {}?"
cmd_inv_none = "You have nothing in your inventory."
movement_wait_local = "You rest for a while."
movement_wait_world = "You wait in the area."
movement_move_error = "You cannot travel there."
movement_move_oob = "You reached the edge of the map."
movement_move_swim = "You cannot swim."
movement_move_block = "You walk into {}."
movement_unit_displace = "The {} switches places with the {}."

movement_move_chars = {
    "=": "furniture",
    "+": "a door",
    "/": "a door",
    "o": "a lamp",
    "#": "a wall",
    "x": "a post",
    "~": "a river",
    "T": "a tree",
    "f": "a tree",
    "Y": "a tree",
    "%": "a wall",
}

interact_door_close_act = "Closing door."
interact_door_close_none = "No open doors next to you."
interact_door_close_many = "There is more than one open door near you. Which door?"
interact_door_close_invalid = "Invalid direction. Canceled closing door."
interact_door_close_error = "Direction has no door. Canceled closing door."
interact_door_open_act = "Opening door."
interact_door_open_none = "No closed doors next to you."
interact_door_open_many = "There is more than one closed door near you. Which door?"
interact_door_open_invalid = "Invalid direction. Canceled opening door."
interact_door_open_error = "Direction has no door. Canceled closing door."

pass_by_item = [
    "You pass by an item.",
    "There is something here."
    "Your feet touches an object."
]

if __name__ == "__main__":
    try:
        print(movement_move_chars[input()])
    except KeyError:
        raise