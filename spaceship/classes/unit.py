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

# self.damage_lower = 1
# self.damage_higher = 2

'''

class Unit(Object):
    '''Object subclass used in the following subclasses:

    NPCS :- Villagers, Soldiers, Innkeepers, Bishops

    Monsters :- Rat, Bat, Orc

    Playables :- Player, Character

    Implements movement and unit interactions
    '''
    unit_id = 0
    # relation = 100

    def __init__(self, x, y, ch="@", fg=Color.white, bg=Color.black, race="human"):
        super().__init__(x, y, ch, fg, bg)
        self.sight = 7
        self.race = race
        self.cur_health = self.max_health = 5
        Unit.unit_id += 1

    def __str__(self):
        return "{}: (x={}, y={}, ch={}, fg={}, bg={}, race={}, sight={}, {}/{})".format(
            self.__class__.__name__, 
            self.x, 
            self.y, 
            self.character,
            self.foreground,
            self.background,
            self.race,
            self.sight,
            self.cur_health,
            self.max_health
        )

    def move(self, dx, dy):
        self.x += dx
        self.y += dy

    def reply(self):
        return "Hello there!"

    def displace(self, other):
        self.position, other.position = other.position, self.position

    def calculate_attack_damage(self):
        return 1

    def calculate_attack_chance(self):
        return choice([0, 1, 2])

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