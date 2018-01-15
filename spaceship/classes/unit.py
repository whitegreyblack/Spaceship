from random import choice
from .object import Object
from .color import Color

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

unit_chars = ('@', 'o', 'r', 'b', 'R', "v", "V", "B", "G", "I", "S")

class Energy:
    tot_energy = 30
    def __init__(self, speed=10):
        self.speed = speed
        self.cur_energy = 0
    
    def gain(self):
        self.cur_energy += self.speed
    
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
                 race="human", rs=0, speed=10):
        super().__init__(x, y, ch, fg, bg)
        self.sight_city = 14
        self.sight_norm = 7
        self.race = race
        self.cur_hp = self.tot_hp = 5
        self.relationship = rs
        self.energy = Energy(speed)
        self.behaviour_score = 0
        Unit.unit_id += 1

    def __str__(self):
        return "{}: (x={}, y={}, ch={}, fg={}, bg={}, race={}, sight={}, speed={}, {}/{})".format(
            self.__class__.__name__, 
            self.x, 
            self.y, 
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
        self.x += dx
        self.y += dy
        
    def reply(self):
        return "Hello there!"

    def displace(self, other):
        self.position, other.position = other.position, self.position
        # other.energy.reset()

    def calculate_attack_damage(self):
        return 1

    def calculate_attack_chance(self):
        return choice([0, 1, 2])

    def direction(self, unit):
        return unit.x - self.x, unit.y - self.y

    def friendly():
        self.relationship >= 0

    def translate_sight(self, x, y):
        sx = self.x - x + self.sight_norm
        sy = self.y - y + self.sight_norm
        return sx, sy

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
                        neighbor = nodeq.node[0] + i, nodeq.node[1] + j

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