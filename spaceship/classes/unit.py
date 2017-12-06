from object import Object
from color import Color
from random import choice
''' TODO: implement unique attributes
self.str, self.agi, self.int
self.armor_type = unarmored, light, medium, heavy, fort/building
self.damage_type = normal, magic, pierce, siege
self.weapon_type = normal, pierce, missle, instant, min, 
self.damage_physical
self.defense_physical
self.damage_magical
self.defense_magical

# self.exp = 0
# self.job = job
# self.race = race
# self.color = color
# self.health = 10
# self.sight = 15
# self.movable = True

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

    def __init__(self, x, y, ch="@", fg=Color.white, bg=Color.black):
        super().__init__(x, y, ch, fg, bg)
        Unit.unit_id += 1

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
    unit = Unit(5, 5, '@', '#ffffff', "#000000")
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