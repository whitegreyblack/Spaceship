# collision_system.py

"""Collision system class"""

from .system import System


class CollisionSystem(System):
    def process(self):
        pass

"""
# from old code...
def collision_system(logger, managers):
    for entity_id, collision in managers['collision'].components.items():
        collider = managers['entity'].find(entity_id)
        collider_ai = managers['ai'].find(collider)    
        collider_info = managers['information'].find(collider)
        collider_health = managers['health'].find(collider)
        if collider_health.cur_hp < 1:
            continue

        collidee_entity = managers['entity'].find(collision.collided_entity_id)
        collidee_info = managers['information'].find(collidee_entity)
        collidee_health = managers['health'].find(collidee_entity)
        if collidee_health.cur_hp < 1:
            continue

        collidee_hitpoints = collidee_health.cur_hp
        collidee_health.cur_hp -= 1
        ai = False
        if collider_ai:
            ai = True
        logger.messages.append(
            Message(
                f"{collider_info.name.capitalize()} hit{'s' if ai else ' the'} {collidee_info.name} for 1 damage",
                1
            )
        )
    managers['collision'].components.clear()
"""