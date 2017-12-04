import os
import sys
from typing import Tuple
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))+'/../../')
from spaceship.world import World
from spaceship.item import Armor, Weapon, Item, items
from spaceship.units.unit import Unit
from random import randint, choice
from spaceship.tools import distance
from spaceship.units.player import Player

class Rat(Unit):
    def __init__(self, x, y):
        self.unit_id = Unit.unit_id
        Unit.unit_id += 1
        self.sight = 5
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
    
    '''
    RAT AI:
        Between rat and bat these creatures will probably have the lowest
        ai logic involved excluding slimes.
        It doesn't remember locations or loot since these have no value to
        it. This restrains the logic of the ai to only move and attack
        The main purpose of the rat will be to wander and attack the player
        Only when the rat wanders into another creature or spots the player
        will it become hostile and start its attack phase

    '''
    def acts(self, player, units, items):
        # need a function that returns all units/items/whatever in the 
        # rat line of sight
        for unit in units:
            if unit == player:
                print('player spotted -- going to attack')
                if distance(*self.position(), *unit.position_local()) <= 2:
                    print('player within range of attack -- attacking player')
                    self.attack(unit)
                else:
                    print('player not in range of attack -- moving torward player')
                    self.moving_torwards(unit)
            else:
                print('spotted a non player unit')

    def drops(self):
        if randint(0, 1):
            return Item("rat corpse", "%", "red")
        else:
            return None
    
    def talk(self):
        return "Reeeee!!"

    def attack(self, unit):
        print('ATTACKING')

    def moving_torwards(self, unit):
        dx = unit.x - self.x
        dy = unit.y - self.y
        dt = distance(*self.position(), *unit.position_local())
        x = int(round(dx / dt))
        y = int(round(dy / dt))
        print(x, y)
        self.move(x, y)

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
        self.sight = 5

        self.x, self.y = x, y
        self.xp = 20
        self.health = 5
        self.character = "b"
        self.job = "bat"
        self.race = "monster"
        self.color = "brown"

    def talk(self):
        return "Screech"