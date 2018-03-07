from ecs.ecs import (Entity, Description, Render, Attribute, Health, Mana,
        Position
    )
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

def entity_stat_health():
    e = Entity(components=[
        Description('hero'),
        Render('a'),
        Attribute(5, 0, 0),
        Health(1),
    ])
    print(f"id={e.eid}, unit={e.get_component('health').unit}")

def iterate_component_type():
    entities = set()
    entities.add(Entity(components=[
        Description('hero'),
        Render('a'),
        Position(3, 3)
    ]))
    entities.add(Entity(components=[
        Description('hero'),
        Render('a'),
        Attribute(5, 0, 0),
    ]))
    entities.add(Entity(components=[
        Description('hero'),
        Render('a'),
        Attribute(5, 0, 1),
        Health(1),
        Mana(2),
        Position(4, 5)
    ]))
    for entity in entities:
        if entity.has_component('description'):
            print(entity.eid)
            if entity.has_component('attribute'):
                print(entity.eid)
                if entity.has_component('health'):
                    print(entity.eid)
    print('done')
    for entity in entities:
        if entity.has_components(['health', 'mana']):
            print(entity.eid)
            
    for entity in entities:
        if entity.has_component('position'):
            position = entity.get_component('position')
            position.move(2, 3)
            print(position, entity.get_component('position').position)
    
if __name__ == "__main__":
    entity_stat_health()
    iterate_component_type()