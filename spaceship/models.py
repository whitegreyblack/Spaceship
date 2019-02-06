from dataclasses import dataclass, field

@dataclass
class Equipment:
    head = None
    neck = None
    body = None
    armor = None
    arm_left = None
    hand_left = None
    ring_left = None
    arm_right = None
    hand_right = None
    ring_right = None
    waist = None
    leg_left = None
    leg_right = None
    feet = None

@dataclass
class Inventory:
    __inventory: list = field(default_factory=list)

@dataclass
class Gender:
    gender: str = "M"
    bonus: int = 0

@dataclass
class Race:
    race: str
    location: str
    stats: field(default_factory=dict)
    bonus: field(default_factory=dict)
    gold: int
    skills: field(default_factory=dict)
    equipment: field(default_factory=dict)

@dataclass
class Class:
    occupation: str
    bonuses: field(default_factory=dict)
    equipment: field(default_factory=dict)

if __name__ == "__main__":
    c = Class(occupation='Peon', 
              bonuses={
                  'STR': 3
              }, 
              equipment ={
                  'head': 'helmet'
              })
    print(c)
