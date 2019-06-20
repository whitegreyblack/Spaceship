# collision_system.py

"""Collision system class"""

from ..common import Message
from .system import System
import time
from ecs import Effect

class CollisionSystem(System):
    def process(self):
        entity_manager = self.engine.entity_manager
        collision_manager = self.engine.collision_manager
        health_manager = self.engine.health_manager
        ai_manager = self.engine.ai_manager
        info_manager = self.engine.information_manager
        position_manager = self.engine.position_manager

        for entity_id, collision in collision_manager.components.items():
            # check collider and collidee info
            collider = entity_manager.find(entity_id)
            collider_health = health_manager.find(collider)
            collider_info = info_manager.find(collider)
            if not (collider_health and collider_info):
                continue
            if collider_health.cur_hp < 1:
                continue

            collidee = entity_manager.find(collision.entity_id)
            collidee_health = health_manager.find(collidee)
            collidee_info = info_manager.find(collidee)
            collidee_position = position_manager.find(collidee)
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
            self.engine.render_system.process()
            # self.engine.render_system.process()
        collision_manager.components.clear()
        return True

    def process_collision(self, entity):
        collision = self.engine.collision_manager.find(entity)
        if collision.entity_id > 0:
            collidee = self.engine.entity_manager.find(collision.entity_id)
            health = self.engine.health_manager.find(collidee)
            health.cur_hp -= 1
            self.engine.effect_manager.add(collidee, Effect(char='X'))
            self.engine.logger.add(
                Message("You bump into a unit")
            )
            self.engine.render_system.process()
            print(self.engine.collision_manager.remove(entity))
            return True
        else:
            self.engine.effect_manager.add(None, Effect(char='X'))
            self.engine.logger.add(
                Message("You hit the environment")
            )
            self.engine.render_system.process()
            self.engine.collision_manager.remove(entity)
            return True