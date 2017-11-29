import os
import sys
from typing import Tuple
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))+'/../../')
from spaceship.world import World
from spaceship.item import Armor, Weapon, Item, items
from random import randint

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
        self.sight = 5
        self.movable = True

        self.damage_lower = 1
        self.damage_higher = 2

        ''' TODO: implement unique attributes
        self.str, self.agi, self.int
        self.armor_type = unarmored, light, medium, heavy, fort/building
        self.damage_type = normal, magic, pierce, siege
        self.weapon_type = normal, pierce, missle, instant, min, 
        self.damage_physical
        self.defense_physical
        self.damage_magical
        self.defense_magical
        '''
    def __repr__(self):
        return "{}[{}]: ({},{})".format(self.__class__.__name__, self.character, self.x, self. y)

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

    def calculate_attack_damage(self, other):
        return randint(self.damage_lower, self.damage_higher)

    def calculate_attack_chance(self, other):
        chance = randint(1, 20)
        if chance == 1:
            return 0
        elif chance == 20:
            return 2
        else:
            return 1

    def friendly(self):
        return self.relation > 0

    def gain_exp(self, exp):
        self.exp += exp