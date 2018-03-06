from ecs.ecs import Entity, Description, Render, Attribute, Health
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

def entity_stat_health():
    e = Entity(components=[
        Description('hero'),
        Render('a'),
        Attribute(5, 0, 0),
        Health(1),
    ])
    print(e.get_component('health').unit)

if __name__ == "__main__":
    entity_stat_health()