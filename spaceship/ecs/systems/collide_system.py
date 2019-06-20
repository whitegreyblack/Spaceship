# collision_system.py

"""Collision system class"""

from ..common import Message
from .system import System
import time

class CollisionSystem(System):
    def process(self):
        entity_manager = self.engine.entity_manager
        collision_manager = self.engine.collision_manager
        health_manager = self.engine.health_manager
        ai_manager = self.engine.ai_manager
        info_manager = self.engine.information_manager
        position_manager = self.engine.position_manager

        for entity_id, collision in collision_manager.components.items():
            self.engine.logger.messages.append(
                Message(f"{entity_id} {repr(collision)}", 1)
            )            
            collider = entity_manager.find(entity_id)
            collider_health = health_manager.find(collider)
            collider_info = info_manager.find(collider)
            self.engine.logger.messages.append(
                Message(f"{repr(collider_health)} {repr(collider_info)}", 1)
            )            
            if not (collider_health and collider_info):
                continue
            if collider_health.cur_hp < 1:
                continue
            collidee = entity_manager.find(collision.entity_id)
            collidee_health = health_manager.find(collidee)
            collidee_info = info_manager.find(collidee)
            collidee_position = position_manager.find(collidee)

            self.engine.logger.messages.append(
                Message(f"{repr(collidee_health)} {collidee_info}", 1)
            )            
            if not (collidee_health and collidee_info):
                continue
            if collidee_health.cur_hp < 1:
                continue
            
            hitpoints = collidee_health.cur_hp
            collidee_health.cur_hp -= 1
            effect_x, effect_y = collidee_position.x, collidee_position.y
            self.engine.add_component(collidee, 'effect', '*')
            self.engine.logger.messages.append(
                Message(f"{collider_info.name} deals 1 damage to {collidee_info.name}", 1)
            )
            # self.engine.render_system.render_effects()
            # time.sleep(.1)
            # if collidee_health.cur_hp < 1:
            #     self.engine.graveyard_system.process()
            # self.engine.graveyard_system.process()
            self.engine.render_system.process()
        collision_manager.components.clear()
