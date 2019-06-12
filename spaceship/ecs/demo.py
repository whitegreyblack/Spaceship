# demo

"""Example program for ecs package"""

from entity_manager import EntityManager 
from entity import Entity
from component_manager import ComponentManager
from component import Component

def main():
    emanager = EntityManager()
    entity1 = emanager.create_entity()
    entity2 = emanager.create_entity()
    print(emanager, entity1, entity2) 

if __name__ == "__main__":
    main()

