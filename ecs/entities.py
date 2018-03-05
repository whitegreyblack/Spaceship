from ecs import Entity
import components
from die import Die

def make_sword():
    return Entity(description=components.Description(
            name='sword',
            less='An iron sword.', 
            more='A common weapon used by adventurers.'),
        components={
        'render': components.Render('('),
        'damage': components.Damage('1d6'),
    })

def make_armor():
    return Entity(description=components.Description(name="armor"),
                  components={
                    'render': components.Render(']'),
                    'armor': components.Defense(3),
    })

def make_player(name="Hero"):
    return Entity(description=components.Description(name=name),
        components={
            'render': components.Render('@'),
            'damage': components.Damage('1d4'),
            'armor': components.Defense(2),
        })

def make_enemy(name="rat", symbol="r"):
    return Entity(description=components.Description(name=name),
        components={
            'render': components.Render(symbol),
            'damage': components.Damage('2d3'),
            'armor': components.Defense(1),
        })

if __name__ == "__main__":
    p = make_player()
    print(p)
    s = make_sword()
    print(s)
    a = make_armor()
    print(a)