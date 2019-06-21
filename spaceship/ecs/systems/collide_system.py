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

    def process_collision_entity(self, entity, collision):
        collidee = self.engine.entity_manager.find(collision.entity_id)
        position = self.engine.position_manager.find(collidee)
        health = self.engine.health_manager.find(collidee)
        health.cur_hp -= 1
        self.engine.graveyard_system.process()
        effect = Effect(char='*')
        # if entity == self.engine.player:
        #     self.engine.logger.add("You bump into a unit")
        return Effect(char='*'), position.x, position.y

    def process_collision_environment(self, entity, collision):
        effect = Effect(char='X')
        position = self.engine.position_manager.find(entity)
        movement = self.engine.movement_manager.find(entity)
        # if entity == self.engine.player:
        #     self.engine.logger.add("You bump into a wall")
        return Effect(char='X'), position.x + movement.x, position.y + movement.y

    def process_collision(self, entity):
        environment_collision = False
        collision = self.engine.collision_manager.find(entity)
        if collision.entity_id > -1:
            effect, x, y = self.process_collision_entity(entity, collision)
        else:
            effect, x, y = self.process_collision_environment(entity, collision)
            environment_collision = True
        if entity == self.engine.player:
            self.engine.render_system.render_effect(x, y, effect)
        self.engine.render_system.process()
        # self.engine.graveyard_system.process()
        self.engine.collision_manager.remove(entity)
        if entity == self.engine.player:
            return not environment_collision
        return True
