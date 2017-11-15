import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))+'/../')
from collections import namedtuple
'''
Item class is used in two areas, new character creation screen and new_game 
Each item passed in should hold certain item properties that can be copied
and placed into the item to make a valid item object. If not then a value
error is raised.

Item Classifiers: (-- Based on ADOM item classifiers)
    [  Armor, shields, cloaks, boots, girdles, gauntlets and helmets
    *  Gems
    o  Rocks
    ]  Tools
    '  Necklaces
    (  Melee weapons
    }  Missile weapons
    /  Missiles
    =  Rings
    \  Wands
    !  Potions
    ?  Scrolls
    ~  Bracers
    %%  Food
    $  Gold
    {  Instruments
    "  Books
'''
# seperated by body type then item type for weapons or wearables
# ADOM
# DV - defensive value -- monsters ability to hit player
# PV - protection value -- reduction in damage when hit
# QUD
# PV - penetration value, affects how many times you'll deal damage in a single hit.
# AV - armor value, is compared vs PV to determine how much damage you'll resist.
# DV - dodge value. Attacks need to make an agility check against your DV to determine if they'll hit.
# DOTA 
# MAGICAL/PHYSICAL ARMOR + STATUS RESISTANCE
weapon = namedtuple("weapon", "name placement accuracy damage")
armor = namedtuple("armor", "name hands melee_hit missile_hit dv pv")
items = {
    # TODO -- implement commented items 
    "horned helmet": armor( "horned helmet", "head", (1, 3), (0, 1), 0, 1),
    "metal helmet": armor("metal helmet", "head", (0, 1), (0, 1), 0, 1),
    # leather cap, hood

    "gold necklace": armor("gold necklace", "neck", (0, 1), (0, 0), 0, 0),
    # holy symbol, whistle, amulet of power

    "elven chainmail": armor("elven chainmail", "body", (1, 2), (0, 1), 1, 1),
    "metal armor": armor("metal armor", "body", (1, 2), (0, 1), 0, 1),  

    # thick fur coat, light robe, heavy cloak, leather armor
    # thick fur bracers, leather bracers    
    # cloth gloves, leather gloves

    "long spear": weapon("long spear", "double", 2, (2, 6)),
    "silver sword": weapon("silver sword", "single", 1, (3, 7)),
    "battle axe": weapon("battle axe", "double", -1, (3, 12)),
    "copper pick": weapon("copper pick", "single", 1, (1, 4)),
    "mithril dagger": weapon("mithril dagger", "single", 3, (2, 5)),
    "broadsword": weapon("broadsword", "single", -1, (4, 8)),
    "medium shield": weapon("medium shield", "single", -3, (1, 3)),
    "mace": weapon("mace", "single", -1, (3, 9)),
    "warhammer": weapon("warhammer", "double", -3, (8, 15)),
    # wooden staff, small shield, short bow, quarterstaff, long sword
    # ring of earth, ring of nature, ring of power, ring of regen, ring of protection
    # ring of light, ring of ice, ring of resistance, ring of fire, ring of water
    # leather belt, rope belt
    # common pants
    # leather boots, metal boots, sandals
    # tome, spellbook, scrolls
}
def get_all_items():
    for key in items.keys():
        print(items[key])

def check_item(classifier, item):
    try:
        print(items[classifier][item])
    except KeyError:
        raise KeyError("Classifier or item name is wrong")

class Item:
    def __init__(self, name, char, color):
        self.name = name
        self.char = char
        self.color = color
    
class Weapon(Item):
    def __init__(self, name, char, color):
        super().__init__(name, char, color)


if __name__ == "__main__":
    # check_item("head", "horned helmet")
    get_all_items()