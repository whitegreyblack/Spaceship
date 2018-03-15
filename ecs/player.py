# create player
from ecs.ecs import Entity
from ecs.ecs import Information, Equipment, Backpack
def player(info, character):
    e = Entity()
    e.information = Information(*info)
    e.attributes = (10, 10, 10)
    e.equipment = Equipment()
    e.backpack = []
    return e

if __name__ == "__main__":
    hero = player(("Grey", "Human"), None)