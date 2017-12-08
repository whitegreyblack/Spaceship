from typing import Tuple
from random import randint

from .color import Color
from .unit import Unit
from .world import World
from .item import Armor, Weapon, Item, items

# class RelationTable:
#     def __init__(self, unit):
#         pass

#     def calculate_relations(self):
#         pass

# Player should inherit from unit just so evaluation makes
# it so that player evaluates to a unit just like every other
# unit 
class Player(Unit):
    parts=("eq_head", "eq_neck", "eq_body", "eq_arms", "eq_hands", 
           "eq_hand_left", "eq_hand_right", "eq_ring_left", 
           "eq_ring_right", "eq_waist", "eq_legs", "eq_feet")
    def __init__(self, character):
        '''Unpacks the character tuple and calculates stats

        Initial position for world and locations are set here
        as well as the bonuses from race, gender and class
        '''
        super().__init__(0, 0, race=character.race)
        self.exp = 0
        self.level = 1
        self.job = character.job
        self.gold = character.gold
        self.gender = character.gender
        self.skills = character.skills
        self.advexp = self.level * 150

        self.base_stats = character.stats
        self.job_bonus = character.jbonus
        self.race_bonus = character.rbonus
        self.equipment = character.equipment
        self.inventory = character.inventory
        self.gender_bonus = character.gbonus
        self.name = character.name[0].upper() + character.name[1:]

        # functions after unpacking
        self.setup(character.home)
        self.convert_equipment()
        self.convert_inventory()
        self.calculate_initial_stats()
        self.calculate_attack_variables()

    def setup(self, home: str) -> None:
        self.home, self.hpointer = home, World.capitals(home)
        self.wx, self.wy = self.hpointer
        self.wz = 0

    def __str__(self):
        return self.name

    def convert_equipment(self):
        '''Transforms equipment tuples into actual item objects'''
        for p, part in enumerate(self.parts):
            if isinstance(self.equipment[p], list):
                # No item is set for the current body part
                setattr(self, part, None) 
            else:
                # There exists an item -- see if it is defined in the items table already
                # if defined: create the item, else just set the part to the tuple
                try:
                    setattr(self, part, items[self.equipment[p]])
                except KeyError:
                    setattr(self, part, self.equipment[p])

    def convert_inventory(self):
        '''Transforms inventory tuples into actual item objects'''
        for index, item in enumerate(self.inventory):
            try:
                self.inventory[index] = items[item]
            except KeyError:
                pass

    def get_equipment(self):
        for index, part in enumerate(self.parts):
            yield index, part.replace("eq_","").replace("_", " "), getattr(self, part)

    def get_inventory(self):
        for index, item in enumerate(self.inventory):
            yield index, item

    def get_profile(self):
        string_1='''
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
        '''[1:]

        string_2='''
Damage   : {dmg:>6}
Accuracy : {acc:>5}
        '''[1:]
        return (string_1.format(
            *self.get_attribute_stats(),
            name=self.name,
            sex=self.gender,
            race=self.race,
            job=self.job), 
            string_2.format(
                dmg="(" + str(self.damage_lower) + ", " + str(self.damage_higher) + ")",
                acc=self.damage_accuracy))

    def calculate_initial_stats(self) -> None:
        stats = tuple(s + g + r + c for s, g, r, c
                            in zip(self.base_stats,
                                   self.gender_bonus,
                                   self.race_bonus,
                                   self.job_bonus))

        self.str, self.con, self.dex, self.int, self.wis, self.cha = stats
        self.cur_health = self.max_health = self.str + self.con * 2
        self.mp = self.total_mp = self.int * self.wis * 2
        self.sp = self.dex // 5

    def get_attribute_stats(self):
        return self.str, self.con, self.dex, self.int, self.wis, self.cha

    def calculate_attack_variables(self):
        # two items
        self.damage_accuracy = 0
        self.damage_lower = 0
        self.damage_higher = 0

        if self.eq_hand_left:
            self.damage_accuracy += self.eq_hand_left.accuracy
            self.damage_lower += self.eq_hand_left.damage_lower
            self.damage_higher += self.eq_hand_left.damage_higher

        if self.eq_hand_right:
            self.damage_accuracy += self.eq_hand_right.accuracy
            self.damage_lower += self.eq_hand_right.damage_lower
            self.damage_higher += self.eq_hand_right.damage_higher

    def calculate_attack_chance(self):
        '''Returns 0 for miss, 1 for regular hit, 2 for critical'''
        for var in ('damage_accuracy', 'damage_lower', 'damage_higher'):
            if not hasattr(self, var):
                raise AttributeError("Attack Variables not set")
        chance = randint(0, 20) + self.damage_accuracy
        if chance <= 1:
            return 0
        elif chance >= 20:
            return 2
        else:
            return 1

    def calculate_attack_damage(self):
        return randint(self.damage_lower, self.damage_higher) + max(self.str, self.dex)

    def gain_exp(self, exp):
        self.exp += exp

    def check_exp(self):
        if self.exp >= self.advexp:
            self.level += 1
            self.exp = 0
            self.advexp = self.level * 150
            return True
        return False

    def height(self) -> int:
        return self.wz
        
    def move_height(self, move: int) -> None:
        def check_height(move: int) -> int:
            return max(self.wz + move, -1)
        self.wz = check_height(move)
    
    def ascend(self) -> None:
        self.wz = max(self.wz + 1, -1)
    
    def descend(self) -> None:
        self.wz = max(self.wz - 1, -1)

    @property
    def location(self) -> Tuple[int, int]:
        '''returns global position on the world map'''
        return self.wx, self.wy

    @location.setter
    def location(self, location: Tuple[int, int]) -> None:
        '''sets global position given a tuple(x,y)'''
        self.wx, self.wy = location    

    def travel(self, dx: int, dy: int) -> None:
        self.location = (self.wx + dx, self.wy + dy)

    def save_location(self) -> None:
        self.last_position_global = self.location
    
    def get_position_global_on_enter(self) -> Tuple[float, float]:
        def direction(x: float, y: float) -> Tuple[float, float]:
            '''Normalizes the position of the coordinates from 0 to 1'''
            return (x + 1) / 2, (y + 1) / 2

        if not hasattr(self, "last_position_global"):
            raise AttributeError("No last position global variable")
        try:
            return direction(
                self.last_position_global[0] - self.wx, 
                self.last_position_global[1] - self.wy)
        
        except KeyError:
            raise KeyError("Error in -directions-")

    def save_position_local(self) -> None:
        self.last_position_local = self.x, self.y

    def dump(self) -> str:
        '''Prints out player information to terminal'''

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

        return dump_template.format(
            self.name,
            self.gender,
            self.race,
            self.job,
            self.level,
            self.exp)
'''
class Character(Object):
    def __init__(self, n, x, y, i, c='white', r='human', m=10, s=10, b=6, l=5):
        super().__init__(n, x, y, i, c, r)
        self.m=m
        self.s=s
        self.l=l
        self.inventory = Inventory(b)
        self.backpack = Backpack()
'''
if __name__ == "__main__":
    pass