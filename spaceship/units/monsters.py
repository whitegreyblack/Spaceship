import os
import sys
from typing import Tuple
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))+'/../../')
from spaceship.world import World
from spaceship.item import Armor, Weapon, Item, items
from spaceship.units.unit import Unit
from random import randint

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
        self.damage_lower = 3
        self.damage_higher = 5

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