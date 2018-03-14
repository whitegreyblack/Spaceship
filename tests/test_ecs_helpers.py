from ecs.game import has
from ecs.ecs import Entity, Component, Position, Render
import pytest

@pytest.fixture
def entity():
    return Entity(components=[
        Position(3, 4),
        Render('@'),
    ])

def test_is_entity(entity):
    assert isinstance(entity, Entity)

def test_no_args(entity):
    assert has(entity, components=[]) == True

def test_single_args(entity):
    assert has(entity, components=Position) == True
    assert has(entity, components=[Position]) == True
    assert has(entity, components=[Render]) == True

def test_multiple_args(entity):
    assert has(entity, components=[Position, Render]) == True

def test_non_component_arg():
    e = Entity(components=[('delete', False)])
    assert has(e, ['delete'])
    assert has(e, 'delete')

def test_addon_after(entity):
    entity.delete = True
    assert has(entity, 'delete')
'''
# >>> e = Entity(components=[Description('hero'),])
# >>> e, Entity.compdict
# (hero, {'description': {0: Description(unit=hero, name=hero)}})
# >>> e.has_component('description')
# True
# >>> e.get_component('description')
# Description(unit=hero, name=hero)
# >>> e.del_component('description')
# >>> e.has_component('description')
# False
# >>> list(e.components)
# []
>>> e=Entity(components=[Render('@')])
>>> e.render
'''