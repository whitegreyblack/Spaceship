# create player
from ecs.ecs import Entity
from ecs.ecs import (
    Information, Equipment, Backpack, Attribute, Render, Position, Damage
)

def weapon():
    e = Entity()
    e.render = Render(')')
    e.information = Information(name="sword")
    e.damage = Damage(("2d5", Damage.PHYSICAL))
    return e

def player(info, character):
    e = Entity()
    # Render(symbol, foreground, background)
    e.render = Render('@')
    # Position(x, y)
    e.position = Position(3, 4)
    # Damage(damage)
    e.damage = Damage(("1d2", Damage.PHYSICAL))
    # Information(name, race, gender, class)
    e.information = Information(*info)
    # Attributes(strength, agility, intelligence)
    e.attribute = Attribute(10, 10, 10)
    # Equipment(left hand, right hand, body)
    e.equipment = Equipment()
    # Backpack(itemlist)
    e.backpack = Backpack(backpack=[weapon()])
    print(repr(e), e.attribute.health.cur_hp)
    return e

if __name__ == "__main__":
    hero = player(("Grey", "Human"), None)