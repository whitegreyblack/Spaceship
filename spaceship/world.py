# world.py

"""World created using ecs systems"""

from classes.utils import dimensions
from ecs.component_manager import ComponentManager
from ecs.components.position import Position
from ecs.components.render import Render
from ecs.entity import Entity
from ecs.entity_manager import EntityManager

m = """
###########
#...#.....#
###+#.....#
#.........#
###########"""[1:]

def render_world(world, em, pm, rm):
    for e in em.entities:
        position = pm.find(e)
        render = rm.find(e)
        if position and render:
            world[position.y][position.x] = render.char

def main():
    world, width, height = dimensions(m)

    em = EntityManager()
    entity = em.create_entity()

    pm = ComponentManager(Position)
    pm.add(entity, Position(5, 3))

    rm = ComponentManager(Render)
    rm.add(entity, Render())

    render_world(world, em, pm, rm)
    print('\n'.join(''.join(row) for row in world))

if __name__ == "__main__":
    main()
