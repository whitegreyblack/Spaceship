import os
import sys
from typing import Tuple
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))+'/../')
from spaceship.world import World
from spaceship.item import items, Item
from random import randint

class RelationTable:
    def __init__(self, unit):
        pass

    def calculate_relations(self):
        pass

class Unit:
    unit_id = 0
    relation = 100
    def __init__(self, x, y, race, job, char, color):
        self.unit_id = Unit.unit_id
        Unit.unit_id += 1

        self.x, self.y = x, y
        self.character = char
        self.exp = 0
        self.job = job
        self.race = race
        self.color = color
        self.health = 10
        self.movable = True

    def __repr__(self):
        return "{}[{}]: ({},{})".format(self.description, self.character, self.x, self. y)

    def position(self):
        return self.x, self.y

    def move(self, dx, dy):
        self.x += dx
        self.y += dy

    def talk(self):
        return self.job + ': Hello there.'

    def draw(self):
        return self.x, self.y, self.char, self.color

    def displace(self, other, x, y):
        self.move(x, y)
        other.move(-x, -y)

    def attack(self, other):
        pass

    def friendly(self):
        return self.relation > 0

    def gain_exp(self, exp):
        self.exp += exp

class Player:
    parts=("eq_head", "eq_neck", "eq_body", "eq_arms", "eq_hands", 
           "eq_hand_left", "eq_hand_right", "eq_ring_left", 
           "eq_ring_right", "eq_waist", "eq_legs", "eq_feet")
    def __init__(self, character):
        '''Unpacks the character tuple and calculates stats

        Initial position for world and locations are set here
        as well as the bonuses from race, gender and class
        '''
        # unpack everything here
        self.unit_id = -1
        self.exp = 0
        self.level = 1
        self.sight = 5
        self.advexp = self.level * 150
        self.job = character.job
        self.race = character.race
        self.gold = character.gold
        # self.color = None
        # self.character = None
        self.gender = character.gender
        self.skills = character.skills
        self.base_stats = character.stats
        self.job_bonus = character.jbonus
        self.race_bonus = character.rbonus
        self.equipment = character.equipment
        self.inventory = character.inventory
        self.gender_bonus = character.gbonus
        self.name = character.name[0].upper() + character.name[1:]

        # functions after unpacking
        self.setup(character.home)
        self.set_equipment()
        self.calculate_initial_stats()
        self.calculate_attack_variables()

    def setup(self, home: str) -> None:
        self.home, self.hpointer = home, World.capitals(home)
        self.wx, self.wy = self.hpointer
        self.wz = -1

    def set_equipment(self):
        for p, part in enumerate(self.parts):
            if isinstance(self.equipment[p], list):
                setattr(self, part, None) 
            else:
                try:
                    setattr(self, part, items[self.equipment[p]])
                except KeyError:
                    setattr(self, part, self.equipment[p])

        # for part in self.parts:
        #     if hasattr(self, part):
        #         print(part, getattr(self, part))
        #     else:
        #         print(part, hasattr(self, part))


    def calculate_initial_stats(self) -> None:
        stats = tuple(s + g + r + c for s, g, r, c
                            in zip(self.base_stats,
                                   self.gender_bonus,
                                   self.race_bonus,
                                   self.job_bonus))

        self.str, self.con, self.dex, self.int, self.wis, self.cha = stats
        self.hp = self.total_hp = self.health = self.str + self.con * 2
        self.mp = self.total_mp = self.int * self.wis * 2
        self.sp = self.dex // 5

    def calculate_attack_variables(self):
        # two items
        if self.eq_hand_left and self.eq_hand_right:
            self.damage_accuracy = self.eq_hand_left.accuracy + self.eq_hand_right.accuracy
            self.damage_lower = self.eq_hand_left.damage[0] + self.eq_hand_right.damage[0]
            self.damage_higher = self.eq_hand_left.damage[1] + self.eq_hand_right.damage[1]
        elif self.eq_hand_left and not self.eq_hand_right:

            self.damage_accuracy = self.eq_hand_left.accuracy
            self.damage_lower = self.eq_hand_left.damage[0]
            self.damage_higher = self.eq_hand_left.damage[1]
        elif not self.eq_hand_left and self.eq_hand_right:
            self.damage_accuracy = self.eq_hand_right.accuracy
            self.damage_lower = self.eq_hand_right.damage[0]
            self.damage_higher = self.eq_hand_right.damage[1]
        else:
            self.damage_accuracy = 0
            self.damage_lower = 1
            self.damage_higher = 2

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

    def position_global(self) -> Tuple[int, int]:
        return self.wx, self.wy

    def travel(self, dx: int, dy: int) -> None:
        self.wx += dx
        self.wy += dy

    def save_position_global(self) -> None:
        self.last_position_global = self.wx, self.wy
    
    def get_position_global_on_enter(self) -> Tuple[float, float]:
        def direction(x: float, y: float) -> Tuple[float, float]:
            '''Normalizes the position of the coordinates from 0 to 1'''
            return (x + 1) / 2, (y + 1) / 2

        if not hasattr(self, "last_position_global"):
            raise AttributeError("No last position global variable")
        try:
            return direction(
                self.last_position_global[0]-self.wx, 
                self.last_position_global[1]-self.wy)
        
        except KeyError:
            raise KeyError("Error in -directions-")

    def position_local(self) -> Tuple[int, int]:

        return self.mx, self.my

    def move(self, dx: int, dy: int) -> None:

        self.mx += dx
        self.my += dy

    def save_position_local(self) -> None:

        self.last_position_local = self.mx, self.my

    def reset_position_local(self, x: int, y: int) -> None:

        self.mx, self.my = x, y

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
            Head     :
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

class Shopkeeper(Unit):
    def __init__(self, x, y, race, job, char, color):
        super().__init__(x, y, race, job, char, color)
        self.moveable = False
        
    def talk(self):
        return "{}: What you looking for?".format(self.__class__.__name__)

class Innkeeper(Unit):
    def __init__(self, x, y, race, job, char, color):
        super().__init__(x, y, race, job, char, color)
        self.movable = False

    def talk(self):
        return "{}: Need a room to stay?".format(self.__class__.__name__)

class Bishop(Unit):
    def __init__(self, x, y, race, job, char, color):
        super().__init__(x, y, race, job, char, color)

    def talk(self):
        return "{}: Blessings. Need some healing?".format(self.__class__.__name__)

class Soldier(Unit):
    def __init__(self, x, y, race, job, char, color):
        super().__init__(x, y, race, job, char, color)

    def talk(self):
        return "{}: Don't be causing trouble. Move along.".format(self.__class__.__name__)

class Rat(Unit):
    def __init__(self, x, y):
        self.unit_id = Unit.unit_id
        Unit.unit_id += 1

        self.x, self.y = x, y
        self.xp = 25
        self.health = 5
        self.character = "r"
        self.job = "rat"
        self.race = "monster"
        self.color = "brown"
        self.relation = -100

    def drops(self):
        if randint(0, 1):
            return Item("rat corpse", "%", "red")
        else:
            return None
    
    def talk(self):
        return "Reeeee!!"

class GiantRat(Unit):
    def __init__(self, x, y):
        self.x, self.y = x, y
        self.xp = 35
        self.health = 10
        self.character = "r"
        self.job = "giant rat"
        self.race = "monster"
        self.color = "brown"        

    def talk(self):
        return "Screeeee!!"

class Bat(Unit):
    def __init__(self, x, y):
        self.unit_id = Unit.unit_id
        Unit.unit_id += 1

        self.x, self.y = x, y
        self.xp = 20
        self.health = 5
        self.character = "b"
        self.job = "bat"
        self.race = "monster"
        self.color = "brown"

    def talk(self):
        return "Screech"

class Object:
    def __init__(self, n, x, y, i, c='white', r="human", h=10):
        """@parameters :- x, y, i, c
            x: positional argument,
            y: positional argument,
            i: char/image for object representation,
            c: color for object fill
        """
        self.name = n
        self.x = x
        self.y = y
        self.i = i
        self.c = c
        self.r = r
        self.h = h
        self.message = "Im just an object"

    def move(self, dx, dy):
        self.x += dx
        self.y += dy

    def talk(self):
        return self.name + ": " +self.message


class Character(Object):
    def __init__(self, n, x, y, i, c='white', r='human', m=10, s=10, b=6, l=5):
        super().__init__(n, x, y, i, c, r)
        self.m=m
        self.s=s
        self.l=l
        self.inventory = Inventory(b)
        self.backpack = Backpack()
