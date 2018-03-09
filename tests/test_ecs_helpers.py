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
    assert has(entity, components=[Position.name()]) == True
    assert has(entity, components=[Render.name()]) == True
    assert has(entity, components=[Ai.name()]) == False


def test_multiple_args(entity):
    assert has(entity, components=[Position.name(), Render.name()]) == True
    assert has(entity, components=[Position.name(), Ai.name()]) == False


