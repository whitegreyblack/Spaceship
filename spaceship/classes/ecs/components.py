# components.py
from component import Component
from ..die import Die
'''
Entities: name, id
    Tile: render, position
        Floor, Wall, Door
    Unit: render, position, mover, health
        Hero, Enemy
    Item: render, damage, armor
        Sword, Wand

Component List:
    Stats: [s | c | a | i | w | l]
    Mover
    Damage:
        Type (physical, magical, pure)
        Range
    Energy:
        Total
        Current
        Refresh
    Health:
        Total
        Current
        Refresh
    Mana:
        Total
        Current
        Refresh
'''
class Damage(Component):
    def __init__(self, damage):
        self.damage = 

class Health(Component):
    def __init__(self):
        self.max_hp = self.cur_hp = 0
    
    def __str__(self):
        return f"Health: {self.cur_hp}/{self.max_hp}"

    # def status_bonuses(self, strbon, conbon):
    #     self.mod_hp = strbon + conbon * 2
    #     self.max_hp = self.cur_hp = self.hp + self.mod_hp

    # def take_damage(self, heal):
    #     self.hitpoints += damage

    # def heal_damage(self, heal):
    #     self.hitpoints += heal

# class Mana(Component):
#     mp = 5
#     def __init__(self):
#         self.max_mp = self.cur_mp = 0
    
#     def __str__(self):
#         return f"Mana: {self.cur_mp}/{self.max_mp}"

#     def status_bonuses(self, intbon, wisbon):
#         self.mod_mp = intbon + wisbon * 2
#         self.max_mp = self.cur_mp = self.mp + self.mod_mp

#     def use_points(self, usage):
#         self.cur_mp -= usage
    
#     def gain_points(self, regen):
#         self.cur_mp += usage