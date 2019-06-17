# demo

"""Example program for ecs package"""

from entity_manager import EntityManager 
from entity import Entity
from component_manager import ComponentManager
from components.component import Component
from components.position import Position
from components.health import Health

def setup_entities(manager, entity_count):
    for e in range(entity_count):
        yield manager.create_entity()

def move_system(emanager, pmanager):
    for entity in emanager.entities:
        p = pmanager.find(entity)
        if p:
            if p.x > 0:
                p.x -= 1
            if p.y > 0:
                p.y -= 1

def health_system(emanager, hmanager):
    for entity in emanager.entities:
        h = hmanager.find(entity)
        if h is not None and h.cur_hp > 0:
            h.cur_hp -= 1

def main():
    emanager = EntityManager()
    entity1, entity2 = setup_entities(emanager, 2)
    print(emanager, entity1, entity2) 

    cmanager = ComponentManager(Component)
    component1 = Component()
    component2 = Component()
    print(cmanager, component1, component2)

    cmanager.add(entity1, component1)
    cmanager.add(entity2, component2)
    print(cmanager)
    
    print(f"Find entity1(id=1): {cmanager.find(entity1)}")
    print(f"Find entity2(id=2): {cmanager.find(entity2)}")

    print(f"Remove entity1")
    cmanager.remove(entity1)
    print(f"Find entity1(id=1): {cmanager.find(entity1)}")
    print(cmanager, cmanager.components)

    pmanager = ComponentManager(Position)
    position1 = Position(3, 5)
    position2 = Position(6, 1)
    print(pmanager, position1, position2)

    pmanager.add(entity1, position1)
    pmanager.add(entity2, position2)
    print(pmanager)

    for eid in emanager.entities:
        print(eid, pmanager.find(eid))

    while not all((p.x, p.y) == (0, 0) for p in pmanager.components.values()):
        move_system(emanager, pmanager)
        print(pmanager.components)

    hmanager = ComponentManager(Health)
    health1 = Health()
    health2 = Health()
    print(hmanager, repr(health1), repr(health2))

    hmanager.add(entity1, health1)
    hmanager.add(entity2, health2)
    print(hmanager)    

    for eid in emanager.entities:
        print(eid, hmanager.find(eid))

    while not all(h.cur_hp == 0 for h in hmanager.components.values()):
        health_system(emanager, hmanager)
        print(hmanager.components)


def check_component_type():
    manager = ComponentManager(Position)
    e = Entity(1)
    p = Position()
    h = Health()
    manager.add(e, p)
    print(manager, manager.components)
    try:
        manager.add(e, h)
        print(manager, manager.components)
    except:
        print("ValueError handled when adding health into position manager")

if __name__ == "__main__":
    # main()
    check_component_type()
