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
from collections import namedtuple

class Rat(Unit):
    def __init__(self, x, y):
        self.unit_id = Unit.unit_id
        Unit.unit_id += 1
        self.sight = 7
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
    AI Behaviours:
        wander -> goto random point using a* search from current position to point
        follow -> goto specific point using a* search from current position to point/unit
        attack -> fight unit in a specific manner depending on range or melee distance
    RAT AI:
        Between rat and bat these creatures will probably have the lowest
        ai logic involved excluding slimes.
        It doesn't remember locations or loot since these have no value to
        it. This restrains the logic of the ai to only move and attack
        The main purpose of the rat will be to wander and attack the player
        Only when the rat wanders into another creature or spots the player
        will it become hostile and start its attack phase

    '''
    def path(self, p1, p2, tiles):
        '''A star implementation'''
        print(p1, p2)
        node = namedtuple("Node", "df dg dh parent node")
        openlist = set()
        closelist = []
        openlist.add(node(0, 0, 0, None, p1))
        while openlist:
            nodeq = min(sorted(openlist))
            openlist.remove(nodeq)
            for i in range(-1, 2):
                for j in range(-1, 2):
                    if (i, j) != (0, 0):
                        neighbor = nodeq.node[0]+i, nodeq.node[1]+j
                        print(neighbor)

                        if neighbor == p2:
                            print("found?")
                            closelist.append(nodeq)
                            # closelist.append(neighbor)
                            return closelist

                        if neighbor in tiles.keys() and tiles[neighbor].char not in ("#", "+"):

                            sg = nodeq.dg + int(distance(*nodeq.node, *neighbor) * 10)
                            sh = int(distance(*neighbor, *p2) * 10)
                            sf = sg + sh

                            if any(n.node == neighbor and n.df < sf for n in openlist):
                                pass
                            elif any(n.node == neighbor and n.df < sf for n in closelist):
                                pass
                            else:
                                openlist.add(node(sf, sg, sh, nodeq.node, neighbor))

            closelist.append(nodeq)
        # the final closelist will be all nodes connecting p1 to p2
        return closelist        

    def acts(self, player, tiles, units):
        # need a function that returns all units/items/whatever in the 
        # rat line of sight -- basically a mini dungeon output based on sight
        def build_sight_map():
            def map_out():
                return "\n".join("".join(row) for row in sight_map)
            sight_map[self.sight][self.sight] = self.character
            for (x, y) in tiles:
                if player.position_local() == (x, y):
                    # check if player position is on the tile
                    char = "@"
                    paths.append((100, player, self.path(self.position(), player.position_local(), tiles)))
                elif (x, y) in units.keys():
                    # check if unit is on the square
                    char = units[(x, y)].char
                elif tiles[(x, y)].items:
                    # check for items on the square
                    char = tiles[(x, y)].items[0].char
                else:
                    # empty square
                    char = tiles[(x, y)].char
                # offset the location based on unit position and sight range
                dx, dy = self.x-x+self.sight, self.y-y+self.sight
                sight_map[dy][dx] = char
            # print(map_out())
        # start with an empty sight map
        sight_range = self.sight * 2 + 1
        sight_map = [[" " for x in range(sight_range)] for y in range(sight_range)]
        paths = []
        build_sight_map()
        if not paths:
            # nothing of interest to the rat
            self.wander(tiles)
        else:
            _, interest, path = max(paths)
            print(self.position(), interest, path)
            if len(path) > 2:
                # take the second point since first is the position of the unit
                self.moving_torwards(path[1].node)
            else:
                if isinstance(interest, Unit):
                    self.attack(interest)
                else:
                    self.attack(interest)
        # print(paths)

    def wander(self, tiles):
        print('wandering about')
        self.moving_torwards(choice(list(tiles.keys())))

    def drops(self):
        if randint(0, 5):
            return Item("rat corpse", "%", "red")
        else:
            return None
    
    def talk(self):
        return "Reeeee!!"

    def attack(self, unit):
        print('ATTACKING')

    def moving_torwards(self, unit):
        try:
            dx = unit.x - self.x
            dy = unit.y - self.y
            try:
                dt = distance(*self.position(), *unit.position_local())
            except:
                dt = distance(*self.position(), *unit.position())
        except:
            dx = unit[0] - self.x
            dy = unit[1] - self.y
            dt = distance(*self.position(), *unit)
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