import os
import sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))+'/../')
from typing import Tuple
from spaceship.world import World
# from spaceship.objects import Object, Character

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
        stats = tuple(s + g + r + c for s , g, r, c 
                            in zip(self.base_stats,
                                   self.gender_bonus,
                                   self.race_bonus,
                                   self.job_bonus))
        
        self.str, self.con, self.dex, self.int, self.wis, self.cha = stats
        self.hp = self.total_hp = self.str + self.con * 2
        self.mp = self.total_mp = self.int * self.wis * 2
        self.sp = self.dex // 5

    ###########################################################################
    #
    #   Height - Z Axis Functions
    #
    ###########################################################################
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

    ###########################################################################
    #
    #   Global X, Y Position Coordinate Functions
    #
    ###########################################################################
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
            raise AttributeError("Cant call this func without a last_position_global")
        try:
            return direction(self.last_position_global[0]-self.wx, self.last_position_global[1]-self.wy)
        
        except KeyError:
            raise KeyError("direction not yet added or calculations were wrong")

    ###########################################################################
    #
    #   Local X, Y Position Coordinate Functions
    #
    ###########################################################################
    def position_local(self) -> Tuple[int, int]:
        return self.mx, self.my

    def move(self, dx: int, dy: int) -> None:
        self.mx += dx
        self.my += dy

    def save_position_local(self) -> None:
        self.last_position_local = self.mx, self.my

    def reset_position_local(self, x: int, y: int) -> None:
        self.mx, self.my = x, y

    ###########################################################################
    #
    #   Player Data Print Function
    #
    ########################################################################### 
    def dump(self) -> str:
        GREEN='\x1b[1;32;40m'
        RED='\x1b[1;31;40m'
        BLUE='\x1b[0;34;40m'
        YELLOW='\x1b[0;33;40m'
        
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

        # print(self.backpack.dump())
        return dump_template.format(
            self.name,
            self.gender,
            self.race,
            self.job,
            self.level,
            self.exp)