from collections import namedtuple
from spaceship.classes.die import Die

'''
Item class is used in two areas, new character creation screen and new_game 
Each item passed in should hold certain item properties that can be copied
and placed into the item to make a valid item object. If not then a value
error is raised.

    Item:
        # Holdable -> weapons
        attackable = weapons
        Usable -> tools
        Consumable -> food
        Drinkable -> potions
        Wearable -> armor
        Readable -> books
        Throwable -> missles
        Viewable -> All? (descriptions)
        Castable -> wands

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
    string = ", ".join(f"{modify(e)}:{mark(v)}" for e, v in effects)
    if string:
        return "(" + string + ")"
    else:
        return ""

class Item:
    def __init__(self, name, char, color, 
                 item_type=None, placement=None, effects=None, hands=None):
        self.name = name
        self.char = char
        self.color = color
        self.__effects = effects

        # used in sorting items by type
        self.item_type = item_type

        # equipable
        if placement:
            self.placement = placement

        # holdable
        if hands:
            self.hands = hands

    def __str__(self):
        return f"{self.name} {seperate(self.effects)}"

    def __repr__(self):
        return f"[{self.__class__.__name__}] {self.name} {seperate(self.effects)}"

    @property
    def effects(self):
        if self.__effects:
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

    def use(self, unit):
        for effect, value in self.effects:
            yield effect, value

attrs = "str con dex wis int cha hp mp hr mr sp dv mr".split()

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

    