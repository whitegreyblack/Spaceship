from random import randint, choice
from collections import namedtuple
from typing import Tuple

from ..tools import distance
from .color import Color
from .item import Armor, Weapon, Item, items
from .charmap import item_chars, unit_chars
from ..action import commands_ai
from .unit import Unit

class Rat(Unit):
    def __init__(self, x, y, ch="r", fg=Color.orange_darker, bg=Color.black,
                 race="rat", job="monster", rs=-100, speed="NORMAL"):
        super().__init__(x, y, ch=ch, fg=fg, bg=bg, race=race, rs=-100, speed=speed)
        self.xp = 25
        self.job = "monster"
        self.damage_lower = 3
        self.damage_higher = 5
        self.last_action = None
        self.current_action = None
        self.friendly = False
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

                        if neighbor == p2:
                            # print("found?")
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
        if not openlist:
            # return False or closelist?
            return closelist

        return closelist        

    def acts(self, player, tiles, units):
        # need a function that returns all units/items/whatever in the 
        # rat line of sight -- basically a mini dungeon output based on sight
        def build_sight_map():
            '''purely visual recording of environment -- no evaluation yet'''
            def map_out():
                return "\n".join("".join(row[::-1]) for row in sight_map[::-1])
            sight_map[self.sight][self.sight] = self.character
            spotted = False
            for (x, y) in tiles:
                if player.position == (x, y):
                    # check if player position is on the tile
                    char = "@"
                    spotted = True
                    paths.append((100, player, self.path(self.position, player.position, tiles)))
                elif (x, y) in units.keys():
                    # check if unit is on the square
                    char = units[(x, y)].character
                    # spotted = True
                elif tiles[(x, y)].items:
                    # check for items on the square
                    char = tiles[(x, y)].items[0].char
                else:
                    # empty square
                    char = tiles[(x, y)].char
                # offset the location based on unit position and sight range
                dx, dy = self.x-x+self.sight, self.y-y+self.sight
                sight_map[dy][dx] = char

            if spotted:
                # print(self.energy.speed)
                # print(map_out())
                pass
            
        # start with an empty sight map
        unit_spotted = []
        item_spotted = []
        # maybe traps later

        sight_range = self.sight * 2 + 1 # accounts for radius
        sight_map = [[" " for x in range(sight_range)] for y in range(sight_range)]
        paths = []
        build_sight_map()

        '''So RAT AI starts with evaluating environment first before
        evaluating itself.
        It determines the safety of the environment before making decisions
        if units do not exist -> safe
        If units exist and does not include enemies -> safe
        if units exist and does include enemies -> danger
        Then makes a decision based on dungeon danger
        if safe and need to heal -> heal
        if safe and no need to heal -> wander
        if unsafe and need to heal -> run
        if unsafe and no need to heal -> fight
        '''
        if self.cur_health <= self.max_health * .10:
            # monster is wounded/damaged -- try preserving its life
            # print('Waiting and resting')
            return commands_ai['wait']

        else:
            # monster is healthy -- do monster stuff
            if not paths:
                # nothing of interest to the rat
                if self.last_action == "following":
                    # print('Following trail of last seen unit')
                    self.moving_torwards()
                self.wander(tiles, sight_map)
            else:

                _, interest, path = max(paths)
                # print(self.position, interest, path)
                if not path:
                    # path returns false
                    self.wander(tiles, sight_map)
                # get distance to determine action
                # elif isinstance(interest, Unit) or isinstance(interest, Player):
                elif isinstance(interest, Unit):
                    if self.race in interest.__class__.__name__:
                        # print('Saw another {}'.format(self.race))
                        pass
                    else:
                        dt = distance(*self.position, *interest.position)
                        if dt < 2:
                            # x, y = self.x - interest.x, self.y - interest.y
                            # self.attack(interest)
                            return commands_ai['move'][self.direction(interest)]

                        else:
                            # print("Saw {}".format(interest))
                            self.follow(sight_map, units, path[1].node)
        # print(paths)

    def wander(self, tiles, sight):
        # print('wandering about')
        # filter out all tiles that are not empty spaces
        # do not want to go to tiles containing blockable objects or units
        # so filter twice: once to get floor tiles, again to get empty ones

        # these are all the non wall tiles
        points = list(filter(lambda t: tiles[t].char != "#", tiles.keys()))
        emptys = list(filter(lambda xy: sight[self.y-xy[1]+self.sight][self.x-xy[0]+self.sight] not in unit_chars, points))
        point = choice(emptys)
        self.moving_torwards(point)

    def follow(self, sight, units, path):
        # print('following')
        # print(sight[self.y - path[1] + self.sight][self.x - path[0] + self.sight])
        empty = sight[self.y - path[1] + self.sight][self.x - path[0] + self.sight] not in unit_chars
        if not empty:
            # print('tile not empty')
            # print(units[(path)])
            # print('switching placse with {}'.format(units[(path)]))
            self.displace(units[(path)])
        else:
            # print('empty tile')
            self.moving_torwards(path)
        
    
    def moving_torwards(self, unit):
        try:
            dx = unit.x - self.x
            dy = unit.y - self.y
            try:
                dt = distance(*self.position, *unit.position_local())
            except:
                dt = distance(*self.position, *unit.position)
        except:
            dx = unit[0] - self.x
            dy = unit[1] - self.y
            dt = distance(*self.position, *unit)
        x = int(round(dx / dt))
        y = int(round(dy / dt))
        self.move(x, y)

    def drops(self):
        if randint(0, 5):
            return Item("rat corpse", "%", "red")
        else:
            return None
    
    def talk(self):
        return "Reeeee!!"

    def attack(self, unit):
        # print('ATTACKING')
        chance = self.calculate_attack_chance()
        if chance == 1:
            # print('rat rolls to hit -- rolls a hit')
            damage = self.calculate_attack_damage()
            # print('rat rolls damage -- rolls {}'.format(damage))
            unit.cur_health -= damage
            # print('rat deals {} damage to {}'.format(damage, unit))
            # print('{} has {} health left'.format(unit, unit.cur_health))
            if unit.cur_health <= 0:
                # print('unit has died')
                pass

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

if __name__ == "__main__":
    print('Monsters.py')