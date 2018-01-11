from .unit import Unit
from .color import Color

class Bat(Unit):
    def __init__(self, x, y, ch='b', fg=Color.orange_darkest, bg=Color.black):
        super().__init__(x, y, ch, fg, bg)
        Unit.unit_id += 1

        self.sight_norm = 5
        self.xp = 20
        self.health = 5
        self.character = "b"
        self.job = "bat"
        self.race = "monster"
        self.color = "brown"

    def talk(self):
        return "Screech"

if __name__ == "__main__":
    # Test unit
    unit = Bat(5, 5, '@', '#ffffff', "#000000")
    print(unit)
    unit.move(1, 0)
    print(unit)
    print(unit.reply())
    print(unit.calculate_attack_chance(), unit.calculate_attack_damage())

    a = Bat(5, 5)
    b = Bat(6, 6)
    print(a.distance(b))
    a.displace(b)
    print(a)
    print(b)