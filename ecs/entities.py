from ecs import Entity
import .components
from .die import Die

def make_sword():
    return Entity(components={
        components.Description(
            name='sword',
            less='An iron sword.', 
            more='A common weapon used by adventurers.'),
        components.Render('('),
        components.Damage('1d6'),
    })

def make_armor():
    return Entity(components={
        components.Description(name="armor"),
        components.Render(']'),
        components.Defense(3),
    })

def make_player(name="Hero"):
    return Entity(components={
        components.Description(name=name),
        components.Render('@'),
        components.Damage('1d4'),
        components.Defense(2),
    })

def make_enemy(name="rat", symbol="r"):
    return Entities(components=[
        components.Description(name=name),
        components.Render(symbol),
        components.Damage('2d3'),
        components.Defense(1),
    ])

if __name__ == "__main__":
    p = make_player()
    print(p)
    s = make_sword()
    print(s)
    a = make_armor()
    print(a)