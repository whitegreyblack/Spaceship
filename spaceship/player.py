import os
import sys
from typing import Tuple
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))+'/../')
from world import World

class Unit:
    def __init__(self, x, y, desc, char, color):
        self.x, self.y = x, y
        self.character = char
        self.description = desc
        self.color = color

    def position(self):
        return self.x, self.y

    def move(self, dx, dy):
        self.x += dx
        self.y += dy

    def talk(self):
        return self.name + ': ' + self.message

    def draw(self):
        return self.x, self.y, self.char, self.color

    def __repr__(self):
        return "{}[{}]: ({},{})".format(self.description, self.character, self.x, self. y)

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

class Player:
    def __init__(self, character):
        '''Unpacks the character tuple and calculates stats

        Initial position for world and locations are set here
        as well as the bonuses from race, gender and class
        '''
        # unpack everything here
        self.exp = 0
        self.level = 1
        self.sight = 5
        self.advexp = 80
        self.job = character.job
        self.race = character.race
        self.gold = character.gold
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
        self.calculate_initial_stats()

    def setup(self, home: str) -> None:
        self.home, self.hpointer = home, World.capitals(home)
        self.wx, self.wy = self.hpointer
        self.wz = -1

    def calculate_initial_stats(self) -> None:
        stats = tuple(s + g + r + c for s, g, r, c
                            in zip(self.base_stats,
                                   self.gender_bonus,
                                   self.race_bonus,
                                   self.job_bonus))

        self.str, self.con, self.dex, self.int, self.wis, self.cha = stats
        self.hp = self.total_hp = self.str + self.con * 2
        self.mp = self.total_mp = self.int * self.wis * 2
        self.sp = self.dex // 5

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
