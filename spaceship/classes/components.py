# components.py

class Health:
    hp = 10
    def __init__(self):
        self.max_hp = self.cur_hp = 0
    
    def __str__(self):
        return f"Health: {self.cur_hp}/{self.max_hp}"

    def status_bonuses(self, strbon, conbon):
        self.mod_hp = strbon + conbon * 2
        self.max_hp = self.cur_hp = self.hp + self.mod_hp

    def take_damage(self, heal):
        self.hitpoints += damage

    def heal_damage(self, heal):
        self.hitpoints += heal

class Mana:
    mp = 5
    def __init__(self):
        self.max_mp = self.cur_mp = 0
    
    def __str__(self):
        return f"Mana: {self.cur_mp}/{self.max_mp}"

    def status_bonuses(self, intbon, wisbon):
        self.mod_mp = intbon + wisbon * 2
        self.max_mp = self.cur_mp = self.mp + self.mod_mp

    def use_points(self, usage):
        self.cur_mp -= usage
    
    def gain_points(self, regen):
        self.cur_mp += usage