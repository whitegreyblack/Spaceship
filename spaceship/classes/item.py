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

item_chars = ('[', '*', 'o', '\'', '(', '}', '/', '=', '\\', '!', '?', '%', '$', '"')
# item_chars = ('[', '*', 'o', ']', '\'', '(', '}', '/', '=', '\\', '!', '?', '~', '%', '$', '{', '"')

def totattr(effect):
    return "tot_" + effect

def modattr(effect):
    return "mod_" + effect

def curattr(effect):
    return "cur_" + effect
    
def sort(items):
    # weapons, armors, potions, rings, food, others = [], [], [], [], []
    # seperate each item into its own grouping
    groups = {
        g: [] for g in "weapon armor potion ring food others".split()
    }
    for item in items:
        try:
            group = groups[item.__class__.__name__.lower()]
        except KeyError:
            group = groups['others']
        group.append(item)
    return groups

def mark(value: int) -> str:
    if isinstance(value, int):
        if value >= 0:
            return "+" + str(value)
        else:
            return value
    return value

def modify(value: str) -> str:
    return value.replace('', '')

def seperate(effects):
    return ", ".join(f"{modify(e)}:{mark(v)}" for e, v in effects)

def convert(item):
    try:
        item = itemlist[item]
    except KeyError:
        pass
    except TypeError:
        pass    
    return item

class Item:
    def __init__(self, name, char, color, effects, slots=None):
        self.name = name
        self.char = char
        self.color = color
        self.__effects = effects

    def __str__(self):
        return f"{self.name} ({seperate(self.effects)})"

    def __repr__(self):
        return f"{self.name} ({seperate(self.effects)})"

    @property
    def effects(self):
        for effect, value in self.__effects:
            if effect == 'dmg':
                if not isinstance(value, tuple):
                    value = (value, value)

                for effect, val in zip('dmg_lo dmg_hi'.split(), value):
                    yield effect, val
            else:
                yield effect, value

class Food(Item):
    inventory = "food"
    def __init__(self, name, char, color, effects, turns):
        super().__init__(name, char, color, effects)
        self.turns = turns

    def eat(self):
        for effect, value in self.effects:
            yield effect, value

class Potion(Item):
    inventory = "potions"
    def __init__(self, name, char, color, effects=None):
        super().__init__(name, char, color, effects)

    def __repr__(self):
        return "[Potion] {:<15}: HEAL={}:".format(self.name, self.heal)

    def use(self, unit):
        for effect, value in self.effects:
            yield effect, value

class Shoes(Item):
    inventory = "shoes"
    placement = {"feet"}
    def __init__(self, name, char, color, effects=None):
        super().__init__(name, char, color, effects)

class Ring(Item):
    inventory = "rings"
    placement = {"ring_left", "ring_right"}

    def __init__(self, name, char, color, effects=None):
        super().__init__(name, char, color, effects)
        
class Armor(Item):
    def __init__(self, name, char, color, placement, effects):
        super().__init__(name, char, color, effects)
        self.placement = placement

class Weapon(Item):
    inventory = "weapons"
    placement = {"hand_left", "hand_right"}
    def __init__(self, name, char, color, effects, hands):
        super().__init__(name, char, color, effects)
        self.hands = hands

itemlist = {
    # TODO -- implement shields
    # TODO -- implement ranged weapons
    # TODO -- implement readable items: scrolls, tomes
    "horned helmet": Armor("horned helmet", "[", "grey", "head", 
        (("dv", 1), ("str", 1))),
    "metal helmet": Armor("metal helmet", "[", "grey", "head",
        (("dv", 2), ("str", 1))),
    "leather cap": Armor("leather cap", "[", "grey", "head", 
        (("dv", 1),)),
    "cloth hood": Armor("cloth hood", "[", "grey", "head", 
        (("dv", 1), )),
    "gold necklace": Armor("gold necklace", "'", "yellow", "neck", 
        (("cha", 2),)),
    "holy symbol": Armor("holy_symbol", "'", "white", "neck", 
        (("wis", 2),)),
    # "whistle": Armor("whistle", "'", "grey", 
    #     "neck", 0, 0, 0, 0),
    # "amulet of power": Armor("amulet of power", 
    #     "'", "red", "neck", 0, 0, 0, 0),
    "elven chainmail": Armor("elven chainmail", "[", "blue", "body",
        (("dv", 4), ("mr", -3))),
    # "metal armor": Armor("metal armor", 
    #     "[", "grey", "body", 1, 1, 0, 1),  
    "thick fur coat": Armor("thick fur coat", "[", "grey", "body", 
        (("dv", 2),)),
    "light robe": Armor("light robe", "[", "grey", "body", 
        (("dv", 1),)),
    # "heavy cloak":  Armor("heavy cloak", 
    #     "[", "grey", "body", 0, 0, 0, 0),
    # "leather armor": Armor("leather armor", 
    #     "[", "grey", "body", 0, 0, 0, 0),
    "thick fur bracers": Armor("thick fur bracers", "[", "grey", "body", 
        (("dv", 1),)),
    # "leather bracers": Armor("leather bracers", 
    #     "[", "grey", "body", 0, 0, 0, 0),
    # "cloth gloves": Armor("cloth gloves",
    #     "[", "grey", "body", 0, 0, 0, 0),
    # "leather gloves": Armor("leather gloves",
    #     "[", "grey", "body", 0, 0, 0, 0),
    "long spear": Weapon("long spear", "(", "grey", 
        (("acc", 2), ("dmg", (2, 6))), hands=2),
    # "silver sword": Weapon("silver sword", 
    #     "(", "grey", 1, 1, (3, 7)),
    "battle axe": Weapon("battle axe", "(", "grey",
        (("acc", -1), ("dmg",  (6, 10))), hands=2),
    "copper pick": Weapon("copper pick", "(", "grey",
        (("acc", -2), ("dmg",  (3, 5))), hands=2),
    # "mithril dagger": Weapon("mithril dagger", 
    #     "(", "grey", 1, 3, (2, 5)),
    "broadsword": Weapon("broadsword", "(", "grey", 
        (("acc", 0), ("dmg", (4, 8))), hands=2),
    "long sword": Weapon("long sword", "(", "grey",
        (("acc", 1), ("dmg", (5, 7))), hands=2),
    "medium shield": Weapon("medium shield", "[", "grey",
        (("dv", 2),), hands=1),
    "small shield": Weapon("small shield", "[", "grey", 
        (("dv", 1),), hands=1),
    # "mace": Weapon("mace", 
    #     "(", "grey", 1, -1, (3, 9)),
    # "warhammer": Weapon("warhammer", 
    #     "(", "grey", 2, -3, (8, 15)),
    "wooden staff": Weapon("wooden staff", "(", "grey", 
        (("acc", 3), ("dmg", (3, 5))), hands=2),
    # "quarterstaff": Weapon("quarterstaff", 
    #     "(", "grey", 2, -1, (4, 9)),
    # short bow,
    "ring of earth": Ring("ring of earth", "=", "dark green", 
        (("str", 1),)),
    "ring of nature": Ring("ring of nature", "=", "green", 
        (("wis", 1),)),
    "ring of power": Ring("ring of power", "=", "red", 
        (("str", 2), ("dex", 1))),
    # "ring of regen": None,
    # "ring of protection": None,
    "ring of light": Ring("ring of light", '=', "white", 
        (("wis", 1),)),
    # "ring of chaos": None,
    "ring of ice": Ring("ring of ice", "=", "light blue", 
        (("hp", 10),)),
    "ring of fire": Ring("ring of fire", "=", "dark red", 
        (("dmg", 3),)),
    "ring of water": Ring("ring of water", "=", "dark blue", 
        (("sp", 10),)),
    "ring of lightning": Ring("ring of lightning", "=", "yellow", 
        (("wis", 2),)),
    # "ring of resistance": None,
    # "ring of darkness": None,
    # "storm ring": None,
    "leather belt": Armor("leather belt", "[", "green", "waist", 
        (("dv", 1),)),
    # "rope belt": Armor("rope belt", "[", "green", "waist", 0, 0, 1, 0),
    # "common pants": Armor("common pants", "[", "green", "legs", 0, 0, 0, 0),

    "leather boots": Shoes("leather boots", "[", "green", 
        (("dv", 1),)),
    # "metal boots": Armor("metal boots", "[", "grey", "feet", 0, 0, 0, 0),
    # "sandals": Armor("sandals", "[", "green", "feet", 0, 0, 0, 0),
    # tome, spellbook, scrolls
    "small health potion": Potion("small health potion", "!", "red", 
        (('hp', 5),)),
    # "medium health potion": Potion("medium health potion", "!", "red", 20),
    # "large health potion": Potion("large health potion", "!", "red", 30),
    # "small shield potion": Potion("small shield potion", "!", "blue", 10),
    "berry": Food("berry", "%", "blue", 
        (("hr", 1),), turns=3),
}

def get_all_items():
    for key in items.keys():
        print(itemlist[key].__repr__())

def check_item(classifier, item):
    try:
        print(itemlist[classifier][item])
    except KeyError:
        raise KeyError("Classifier or item name is wrong")

if __name__ == "__main__":
    get_all_items()

'''
Attacking
    Damage Types:
    - Physical, Magical, Pure
    Physical:
        Normal

    Magical:
        Normal - 
        Superior - goes through magic invulnerability
        Holy - only affects holy units
        Demonic - only affects demonic units
        Targeted Type Magic - affects a specific race or gender or job
    Pure:
        Normal Pure - ignores armor and magic resistance completely, affects only health
        Holy Pure - ignores half armor and full magic resistance
        Demonic Pure - ignores full armor and half magic resistance

    Compound:
        Mixed Magical and Physical damage

Defending
    Armor Types:
    - Physical, Magical
    Physical:
        Physical Damage Block - block incoming damage and reduce it by a percentage
        Evasion - ability to evade damage
        Invisibility - Invisible units
        Hidden - Planewalking
        Invulnerability
            Ghost Form - 100% physical invulverability but -100% magic resistance

    Magical:
        Magic Damage Block - block incoming magic damage and reduce it for a flat amount
        Magical Resistance
        Muting - Disables Iventory Abilities
        Silence - Disables Character Abilities
        Invulnerability
        Untargetability

Damage Manipulation:
    Damage Reduction - reduce
    Damage Amplification - amp
        Damage Stacking
    Damage Delay - delay
    Damage Reversal - swap damage for heal
    Damage Reflection - return damage without taking damage
    Damage Return - return damage after taking damage
    Damage Negation - negate any damage and remove damage side effects (poison arrow)
    Damage Refraction - negate any damage but take side effects

    Missle Speed? Probably uneeded
    Attack Range
    Channeling
    Attack Speed/Energy Level

    Physical:
        Piercing - ignores percentage of armor
        Critcal - Critical damage
        Cleave - nearby units get hit after hitting primary enemy (triange)
        Splash - nearby units get hit after hitting primary enemy (circle)
        Lifesteal - take percentage of damage as heal
        Bash - Stuns

    Magical
        Single Target
        Chainable
        AOE:
            Line
            Triangle
            Circle
                Splash
            Global
        Reflective/Bounce
        Timer/Delayed
        Item/Abilty Effects:
            Healing - HOT
            Paralzye - side effect of being electrocuted
            Stunned - cant do any action
            Blinded - cannot target action
            Confused - cannot target action correctly
            Slowed - move slowly
            Poisoned - take damage over time reduced by poison resistance and move slowly
            Burned - take damage over time reduced by fire resistance
            Chill/Freeze - take damage over time reduced by ice resistance
            Crushed - take damage equal to weight of object reduced by physical armor
            Rooted - cannot move but can take other actions
            Knock-Back - moved a single/multiple tiles in the opposite direction of attack
            Hallucinate? - imagine non-existant stuff
            Ghosted - move slowly, cannot attack, can cast spells
            Frozen - cannot move, cannot attack, can cast spells
            Quicken - move faster
            Teleport - move random square in dungeon/map
            Revealed - Position is known to all enemies

EARTH-GREATER flat damage
POISON-Major D.O.T. and minor slow
FIRE-Major DOT and Minor Damage
ICE-Lesser DOT, minor damage, and major SLOW
'''

    