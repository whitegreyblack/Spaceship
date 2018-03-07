from ecs.ecs import (Entity, Description, Render, Attribute, Health, Mana,
        Position, Damage, Defense
    )
import time
import random
# from ecs.components import Health, Attribute, Description, Render

def test_entity():
    e = Entity(components=[Description('hero'),])
    f = Entity(components=[Description('enemy'),])
    for entity in [e, f]:
        assert entity.has_component('description')

def test_entity_components():
    e = Entity(components=[
        Description('hero'),
        Render('@')])
    assert e.has_components(['description', 'render'])

def test_entity_stat_health():
    e = Entity(components=[
        Description('hero'),
        Render('a'),
        Attribute(5, 0, 0),
        Health(1),
    ])
    assert e.has_component('description')
    assert e.has_component('health')
    assert e.get_component('health').cur_hp == 11

    f = Entity(components=[
        Description('hero'),
        Render('a'),
        Health(1),        
        Attribute(5, 0, 0),
    ])
    assert f.has_component('description')
    assert f.has_component('health')
    assert f.get_component('health').cur_hp == 11

    g = Entity(components=[
        Attribute(5, 0, 0),        
        Description('hero'),
        Render('a'),
        Health(1),        
    ])
    assert g.has_component('description')
    assert g.has_component('health')
    assert g.get_component('health').cur_hp == 11

def simulate_fight_simple():
    a = Entity(components=[
        Description('hero'),
        Damage([("2d4", Damage.PHYSICAL)]),
        Health(10),
    ])
    b = Entity(components=[
        Description('enemy'),
        Damage([("1d6", Damage.PHYSICAL)]),
        Health(10)
    ])
    while a.get('health').cur_hp > 0 and b.get('health').cur_hp > 0:
        b.get('health').take_damage(a.get('damage').damage)
        a.get('health').take_damage(b.get('damage').damage)
    if a.get('health').cur_hp > 0:
        print(f"{a.get('description').name} has died")
    else:
        print(f"{b.get('description').name} has died")

def simulate_fight_with_armor():
    a = Entity(components=[
        Description('hero'),
        # Damage([("2d4", Damage.PHYSICAL)]),
        Health(10),
        Defense(1),
    ])
    b = Entity(components=[
        Description('enemy'),
        Defense(2),
        Damage([("1d6", Damage.PHYSICAL)]),
        Health(10)
    ])
    fight(a, b)
    a.add(Damage([("2d4", Damage.PHYSICAL)]))
    fight(a, b)

def fight(a, b):
    def check(unit):
        fightable = unit.has(names=['health', 'damage'])
        if not fightable:
            print(f'{unit} has no health or damage')
        return fightable

    if check(a) and check(b):
        while a.get('health').cur_hp > 0 and b.get('health').cur_hp > 0:
            b.get('health').take_damage(a.get('damage').damage)
            a.get('health').take_damage(b.get('damage').damage)
        if a.get('health').cur_hp <= 0:
            print(f"{a.get('description').name} has died")
        else:
            print(f"{b.get('description').name} has died")

def iterate_component_type():
    entities = set()
    entities.add(Entity(components=[
        Description('hero'),
        Render('a'),
        Position(3, 3)
    ]))
    entities.add(Entity(components=[
        Description('unit'),
        Render('a'),
        Attribute(5, 0, 0),
    ]))
    entities.add(Entity(components=[
        Description('rind'),
        Render('a'),
        Attribute(5, 0, 1),
        Health(1),
        Mana(2),
        Position(4, 5)
    ]))

    for entity in entities:
        print(entity.get_components(['render', 'mana']))
        print(list(entity.components))
        for component in entity.components:
            print(repr(component))

        if entity.has_component('description'):
            print(entity.eid)
            if entity.has_component('attribute'):
                print(entity.eid)
                if entity.has_component('health'):
                    print(entity.eid)

        if entity.has_components(['health', 'mana']):
            print(entity.eid)

def iterate_component_by_entity():   
    t = time.time
    entities = set()
    for i in range(1000):
        e = Entity(components=[Position(0, 0),] if random.randint(0, 1) else [])
        entities.add(e)

    # print(len(entities))
    # print(len([e for e in entities if e.has_component('position')]))
    # count1 = 0
    t1 = t()
    for entity in entities:
        # count1 += 1
        if entity.has_component('position'):
            entity.get_component('position').move(2, 3)
    total1 = t() - t1
    # print(count1)
    print(total1)

    t1 = t()
    for component in Entity.compdict['position'].values():
        component.move(2, 3)
    print(t() - t1)

    count2 = 0
    t1 = t()
    for entity in [e for e in entities if e.has_component('position')]:
        position = entity.get_component('position')
        position.move(2, 3)
    total2 = t() - t1
    print(total2)

    total3 = 0.0
    t1 = t()
    for entity in [e for e in entities if e.has_component('position')]:
        entity.get_component('position').move(2, 3)
    total3 += t() - t1
    print(total3)
    print(total2 > total3)
    return total1 > total2


if __name__ == "__main__":
    # iterate_component_type()
    # print(len([i for i in [iterate_component_by_entity() for _ in range(10000)] if i]))
    iterate_component_by_entity()
    # simulate_fight_simple()
    # simulate_fight_with_armor()