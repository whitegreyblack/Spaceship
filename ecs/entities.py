from ecs import Entity
import components

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

if __name__ == "__main__":
    s = make_sword()
    print(s)
    a = make_armor()
    print(a)
    print(repr(a))