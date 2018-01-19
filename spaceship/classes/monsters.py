from random import randint, choice
from typing import Tuple
from ..tools import distance
from .color import Color
from .item import Armor, Weapon, Item, itemlist, item_chars
from ..action import commands_ai
from .unit import Unit, unit_chars

class Rat(Unit):
    def __init__(self, x, y, ch="r", fg=Color.orange_darker, bg=Color.black,
                 race="rat", job="monster", rs=-100, speed=15):
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

    def acts(self, units, tiles):
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
        # need a function that returns all units/items/whatever in the 
        # rat line of sight -- basically a mini dungeon output based on sight
        def build_sight_map():
            '''purely visual recording of environment -- no evaluation yet'''
            def map_out():
                '''Print out of the current sight map -- useful for debug'''
                return "\n".join("".join(row[::-1]) for row in sight_map[::-1])

            # place self in the middle of the map
            sight_map[self.sight_norm][self.sight_norm] = self.character
            spotted = False

            for tile in tiles:
                # check if unit is on the square
                if tile in units.keys():
                    unit = units[tile]
                    char = unit.character
                    spotted = True
                    # different racial unit
                    if self.character != char:
                        paths.append((100, unit, self.path(self.position, unit.position, tiles)))

                # check for items on the square
                elif tiles[tile].items:
                    char = tiles[tile].items[0].char

                # empty square
                else:
                    char = tiles[tile].char

                # offset the location based on unit position and sight range
                dx, dy = self.translate_sight(*tile)
                sight_map[dy][dx] = char

            if spotted:
                # print(self.energy.speed)
                # print(map_out())
                pass

        paths = []            
        # start with an empty sight map
        unit_spotted = []
        item_spotted = []
        # maybe traps later

        sight_range = self.sight_norm * 2 + 1 # accounts for radius
        sight_map = [[" " for x in range(sight_range)] for y in range(sight_range)]
        build_sight_map()

        # monster is wounded/damaged -- try preserving its life
        # print('Waiting and resting')
        if self.cur_hp <= self.tot_hp * .10:
            return commands_ai['wait']

        # monster is healthy -- do monster stuff
        else:
            # nothing of interest to the rat
            if not paths:
                return self.wander(tiles, sight_map)

            else:
                _, interest, path = max(paths)

                # no path exists
                if not path:
                    return self.wander(tiles, sight_map)

                # get distance to determine action
                # elif isinstance(interest, Unit) or isinstance(interest, Player):
                elif isinstance(interest, Unit):

                    # its another rat -- do nothing
                    if self.race == interest.race:
                        return self.wander(tiles, sight_map)

                    # its another monster -- do nothing
                    elif self.job == interest.job:
                        return self.wander(tiles, sight_map)

                    else:
                        # must be an adventurer -- go for the juggular
                        dt = distance(*self.position, *interest.position)
                        if dt < 2:
                            return commands_ai['move'][self.direction(interest)]
                        # too far -- follow it
                        else:
                            return self.follow(sight_map, units, path[1].node)

    def drops(self):
        if randint(0, 5):
            return Item("rat corpse", "%", "red", (('hp', 2),))
        else:
            return None
    
    def talk(self):
        return "Reeeee!!"

class GiantRat(Unit):
    def __init__(self, x, y):
        self.x, self.y = x, y
        self.xp = 35
        self.hp = 10
        self.character = "r"
        self.job = "giant rat"
        self.race = "monster"
        self.color = "brown"        

    def talk(self):
        return "Screeeee!!"

if __name__ == "__main__":
    print('Monsters.py')

'''
RACE SUB NAME COLOR EXP ITENS
----------------------------
#30D0F0 #000000 monster invertabrate slime 15
#ffffff #000000 monster invertabrate worm 

#904040 #000000 monster rodent rat 10
#904040 #000000 monster rodent bat 10

#307000 #000000 monster reptile snake 15
#307000 #000000 monster repitle lizard 15

#222222 #ffffff monster arachnid spider 5
#222222 #ffffff monster arachnid motherspider 50

human <-> shopowner #C08000 #000000 25
#A04000 #000000 human <-> chieftan 30
#F08000 #000000 human <-> villager 25
human <-> poacher  #306030 #000000 30
human <-> adventurer #408080 #000000 35
human <-> soldier


elven drow lord
elven drow soldier
elven drow villager

elven high lord
elven high soldier
elven high villager

elven wood lord
elven wood soldier
elven wood villager


dwarven lord
dwarven citizen
dwarven soldier
dwarven metalworker
dwarven stoneworker
dwarven woodworker


orcen peon
orcen slave
orcen warrior
orcen warlord


beast aries soldier
beast aries villager

beast capricorn soldier
beast capricorn villager

beast leo soldier
beast leo villager

beast taurus soldier
beast taurus villager


human boss Regulus
beast boss Zorn
orcen boss Ko Mun
elven boss Edochas
dwarf boss Dekay

You are a reincarnated spirit in a new vessel in Calabaston
You choose a new body and birth location

Enemies would be faction related as well an neutral creeps/monsters
Want to do hometown for each faction but might be time consuming
Try hometown of humans first then build outwards

5 serpents? Kings
The main game is to defeat the five legends that aim to bring the factions
to total war leading to annihalation.
These five legends are:
    Zorn - King of Wrath (German) -> Located in Beast Territory | 
    Ko Mun - The Torturer (Korean) -> Ork Territory (vainglory?) | 
    Edochas - The King of Despair (Irish?) -> Elf Forest/Dark Forest (sorrow) |
    Dekay - the Rotten King -> Dwarf (pun) (greed) | 
    Crassus Regulus - the Fat King Gluttony (king of humans) |

# Farm Animals:
Chicken, Cock
Cat
Dog
Sheep
Cow
Horse
# Wilderness Animals:
Rat
Frog
Deer
Snake
Bat
Bee
Spider
Bear
Wolf
Lion
# Racial Factions
Goblins
Dwarves
Ogres -- Cyclops
Orken
Centaurs
Minotaurs
Mud Golem
Treant
Skeleton
Imp
Gnome
Eyeclops
Succubus
Fire Elemental
Earth Elemental
Storm Elemental
Water Elemental
Gorgon
Sphynx
Slime
'''