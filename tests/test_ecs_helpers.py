from ecs.game import has
from ecs.ecs import (
    Entity, Component, Position, Render, Ai, COMPONENTS
)
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
    assert has(entity, components=Position)
    assert has(entity, components=[Position]) == True
    assert has(entity, components=[Render]) == True
    assert has(entity, components=[Ai]) == False


def test_multiple_args(entity):
    assert has(entity, components=[Position, Render]) == True
    assert has(entity, components=[Position, Ai]) == False

def test_non_component_arg():
    e = Entity(components=[('delete', False)])
    assert has(e, ['delete'])
    assert has(e, 'delete')


