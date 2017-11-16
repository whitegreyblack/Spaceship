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
# PV - protection value, affects how many times you'll deal damage in a single hit.
# AV - armor value, is compared vs PV to determine how much damage you'll resist.
# DV - dodge value. Attacks need to make an agility check against your DV to determine if they'll hit.
# DOTA 
# MAGICAL/PHYSICAL ARMOR + STATUS RESISTANCE

# weapon = namedtuple("weapon", "name char color hands accuracy damage")
# armor = namedtuple("armor", "name char color placement melee_hit missile_hit dv pv")

class Item:
    def __init__(self, name, char, color):
        self.name = name
        self.char = char
        self.color = color

    def mark(self, value):
        if isinstance(value, int):
            if value >= 0:
                return "+" + str(value)
            else:
                return value
        return value

    def __str__(self):
        return self.name

class Armor(Item):
    def __init__(self, name, char, color, placement, me_h, mi_h, dv, pv):
        super().__init__(name, char, color)

        self.placement = placement
        self.melee_hit = me_h
        self.missile_hit = mi_h
        self.defensive_value = dv
        self.protection_value = pv

    def __repr__(self):
        return "[{}] {:<15}: HIT=({}, {}), DEF=(DV: {}, PV: {})".format(
            self.__class__.__name__,
            self.name,
            self.mark(self.melee_hit),
            self.mark(self.missile_hit),
            self.mark(self.defensive_value),
            self.mark(self.protection_value))

    def __str__(self):
        return "{} ({}, {})[[{}, {}]]".format(
            self.name,
            self.mark(self.melee_hit),
            self.mark(self.missile_hit),
            self.mark(self.defensive_value),
            self.mark(self.protection_value))

class Weapon(Item):
    def __init__(self, name, char, color, hands, accuracy, damage):
        super().__init__(name, char, color)

        self.hands = hands
        self.accuracy = accuracy
        self.damage_lower, self.damage_higher = damage

    def __repr__(self):
        return "[{}] {:<15}: ACC={}, DMG=({}, {})".format(
            self.__class__.__name__,
            self.name,
            self.mark(self.accuracy),
            self.mark(self.damage_lower),
            self.mark(self.damage_higher))

    def __str__(self):
        return "{} ({}, [[{}, {}]])".format(
            self.name,
            self.mark(self.accuracy),
            self.mark(self.damage_lower),
            self.mark(self.damage_higher))

items = {
    # TODO -- implement commented items 
    "horned helmet": Armor("horned helmet", "[", "grey", "head", 1, 0, 0, 1),
    "metal helmet": Armor("metal helmet", "[", "grey", "head", 1, 0, 0, 1),
    # leather cap, hood

    "gold necklace": Armor("gold necklace", "'", "yellow", "neck", 0, 0, 0, 0),
    # holy symbol, whistle, amulet of power

    "elven chainmail": Armor("elven chainmail", "[", "blue", "body", 2, 1, 1, 1),
    "metal armor": Armor("metal armor", "[", "grey", "body", 1, 1, 0, 1),  

    # thick fur coat, light robe, heavy cloak, leather armor
    # thick fur bracers, leather bracers    
    # cloth gloves, leather gloves

    "long spear": Weapon("long spear", "(", "grey", 2, 2, (2, 6)),
    "silver sword": Weapon("silver sword", "(", "grey", 1, 1, (3, 7)),
    "battle axe": Weapon("battle axe", "(", "grey", 2, -1, (3, 12)),
    "copper pick": Weapon("copper pick", "(", "grey", 1, 1, (1, 4)),
    "mithril dagger": Weapon("mithril dagger", "(", "grey", 1, 3, (2, 5)),
    "broadsword": Weapon("broadsword", "(", "grey", 1, -1, (4, 8)),
    "medium shield": Weapon("medium shield", "[", "grey", 1, -3, (1, 3)),
    "mace": Weapon("mace", "(", "grey", 1, -1, (3, 9)),
    "warhammer": Weapon("warhammer", "(", "grey", 2, -3, (8, 15)),
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
        print(items[key].__repr__())

def check_item(classifier, item):
    try:
        print(items[classifier][item])
    except KeyError:
        raise KeyError("Classifier or item name is wrong")

if __name__ == "__main__":
    # check_item("head", "horned helmet")
    get_all_items()