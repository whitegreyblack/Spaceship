from random import choice
from .object import Object
from .color import Color
from collections import namedtuple
from ..tools import distance
from ..action import commands_ai

''' TODO: implement unique attributes
self.str, self.agi, self.int
self.armor_type = unarmored, light, medium, heavy, fort/building
self.damage_type = normal, magic, pierce, siege
self.weapon_type = normal, pierce, missle, instant, min, 
self.damage_physical
self.defense_physical
self.damage_magical
self.defense_magical
self.damage_lower = 1
self.damage_higher = 2
'''

unit_chars = {'@', 'o', 'r', 'b', 'R', "v", "V", "B", "G", "I", "S"}
unit_chars = set('@ o r b R v V B G S'.split())

class Energy:
    tot_energy = 30
    def __init__(self, speed=10):
        self.speed = speed
        self.cur_energy = 0
    
    def gain(self):
        self.cur_energy += self.speed
    
    @property
    def turns(self):
        return self.cur_energy // self.tot_energy

    def ready(self):
        return self.cur_energy >= self.tot_energy

    def reset(self):
        self.cur_energy -= self.tot_energy

class Unit(Object):
    '''Object subclass used in the following subclasses:

    NPCS :- Villagers, Soldiers, Innkeepers, Bishops

    Monsters :- Rat, Bat, Orc

    Playables :- Player, Character, Hero

    Implements movement and unit interactions
    '''
    unit_id = 0
    # relation = 100
    def __init__(self, x, y, ch="@", fg=Color.white, bg=Color.black, 
                 race="human", rs=0, speed=3):
        super().__init__(x, y, ch, fg, bg)
        self.sight_city = 6
        self.sight_norm = 6
        self.race = race
        self.cur_hp = self.tot_hp = 5
        self.relationship = rs
        self.energy = Energy(speed)
        self.behaviour_score = 0
        Unit.unit_id += 1

    def __str__(self):
        return "{}: (x={}, y={}, ch={}, fg={}, bg={}, race={}, sight={}, speed={}, {}/{})".format(
            self.__class__.__name__, 
            *self.local,
            self.character,
            self.foreground,
            self.background,
            self.race,
            self.sight_norm,
            self.cur_hp,
            self.energy.speed,
            self.tot_hp
        )

    @property
    def is_alive(self):
        '''Checks if current hp is above 0'''
        return self.cur_hp > 0

    def move(self, dx: int, dy: int) -> None:
        '''Adds a vector to current position to change positions'''
        self.local += (dx, dy)
        
    def reply(self):
        return "Hello there!"

    def displace(self, other):
        '''Switches positions of target with self, vice versa'''
        self.local, other.local = other.local, self.local
        # other.energy.reset()

    def direction(self, unit):
        '''Returns a point indicating the vector towards target'''
        return unit.local - self.local

    def calculate_attack_damage(self):
        '''Returns the damage amount of a single hit'''
        return 1

    def calculate_attack_chance(self):
        '''Returns the chance to hit'''
        return 1

    def friendly():
        '''Returns a boolean indicating if unit is friendly'''
        self.relationship >= 0

    def translate_sight(self, x, y):
        '''Offsets input point by current position and sight radius'''
        sight_point = self.local - (x + self.sight_norm, y + self.sight_norm)
        return sight_point

    def moving_torwards(self, point):
        '''Returns the closest 1:1 point torwards input point'''
        dt = self.local.distance(point)
        try:
            dx, dy = point - self.local
        except TypeError:
            dx, dy = point[0] - self.local.x, point[1] - self.local.y

        x = int(round(dx / dt))
        y = int(round(dy / dt))
        return commands_ai['move'][(x, y)]

    def wander(self, tiles, sight):
        # filter out all tiles that are not empty spaces
        # do not want to go to tiles containing blockable objects or units
        # so filter twice: once to get just floor tiles, again to get empty ones

        # these are all the non wall tiles
        points = list(filter(
            lambda t: tiles[t].char != "#", tiles.keys()))

        # # of these points, these are the positions currently empty
        # for point in points:
        #     sx, sy = self.translate_sight(*point)
        #     empty_space = sight[sy][sx] in ". ; : , = /".split()
        #     occupied = sight[sy][sx] in unit_chars

        #     if not empty_space or occupied:
        #         points.remove(point)
            
        # then choose a single point to walk to
        point = choice(points)

        sx, sy = self.translate_sight(*point)
        empty_space = sight[sy][sx] in ". ; : , = /".split()
        occupied = sight[sy][sx] in unit_chars
        
        if not empty_space or occupied:
            return commands_ai['wait']

        return self.moving_torwards(point)  

    def follow(self, sight, units, path):
        sx, sy = self.translate_sight(*path)
        empty_space = sight[sy][sx] not in unit_chars

        # something in the way -- move it
        if not empty_space:
            self.displace(units[path])

        # empty space -- go torward target
        else:
            return self.moving_torwards(path)

    def path(self, p1, p2, tiles):
        '''A star implementation'''
        node = namedtuple("Node", "df dg dh parent node")

        openlist = set()
        closelist = []
        openlist.add(node(0, 0, 0, None, p1))
        while openlist:
            nodeq = min(openlist, key=lambda x: x.df)
            openlist.remove(nodeq)
            
            for i in range(-1, 2):
                for j in range(-1, 2):
                    if (i, j) != (0, 0):
                        neighbor = nodeq.node + (i, j)

                        if neighbor == p2:
                            closelist.append(nodeq)
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

    def within(x, y, lx=6, hx=60, ly=2, hy=20):
        return lx <= x <= hx and ly <= y <= hy

if __name__ == "__main__":
    unit = Unit(x=5, y=5)
    print(unit)
    unit.move(1, 0)
    print(unit)
    print(unit.reply())
    print(unit.calculate_attack_chance(), unit.calculate_attack_damage())

    a = Unit(5, 5)
    b = Unit(6, 6)
    print(a.distance(b))
    a.displace(b)
    print(a)
    print(b)