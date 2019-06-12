# create player
from ecs import Entity
from ecs import (
    Information, Equipment, Inventory, Attribute, Render, Position, Damage,
    Health, Experience, Armor
)

def weapon():
    e = Entity()
    e.render = Render(')')
    e.information = Information(name="sword")
    e.damage = Damage(damages=[
        ("2d5", Damage.PHYSICAL), 
        ("1d6", Damage.MAGICAL)
    ])
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
    e.attribute = Attribute(28, 6, 12)
    # Equipment(left hand, right hand, body)
    e.equipment = Equipment()
    # Backpack(itemlist)
    e.backpack = Inventory(bag=[weapon()])
    print(repr(e), e.attribute.health.cur_hp)
    # e.attribute.modify(stat=('strength', 3))
    print(e.attribute.health)
    e.attribute.health.take_damage(10)
    print(e.attribute.health)
    e.attribute.update()
    print(e.attribute.health)
    e.attribute.update()
    print(e.attribute.health)
    print(e.attribute)
    e.attribute.modify(('strength', 3))
    print(e.attribute)
    return e

def calculate(cls, attr):
    for i in range(100):
        print(f"{i:2}: {getattr(cls(i), attr)}")

if __name__ == "__main__":
    hero = player(("Grey", "Human"), None)
    print(hero)
    # calculate(Health, 'cur_hp')
    # calculate(Experience, 'exp_needed')
    # calculate(Armor, 'max_armor')
