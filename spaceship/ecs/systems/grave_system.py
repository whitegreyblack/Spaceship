# grave_system

"""Graveyard system class"""

from ..common import Message
from .system import System
import time

alive = lambda message: message.lifetime > 0

class GraveyardSystem(System):
    def remove_effects(self):
        self.engine.effect_manager.components.clear()

    def remove_unit(self, entity):
        self.engine.collision_manager.remove(entity)
        self.engine.position_manager.remove(entity)
        self.engine.health_manager.remove(entity)
        self.engine.render_manager.remove(entity)
        self.engine.ai_manager.remove(entity)
        self.engine.entity_manager.remove(entity)

    def remove_units(self):
        # remove 'dead' entities
        entity_manager = self.engine.entity_manager
        health_manager = self.engine.health_manager
        info_manager = self.engine.information_manager
        entites_to_remove = []
        for entity_id, health in health_manager.components.items():
            entity = entity_manager.find(entity_id)
            info = info_manager.find(entity)
            if health.cur_hp < 1:
                entites_to_remove.append(entity)
        for entity in entites_to_remove:                
            self.remove_unit(entity)
            if entity == self.engine.player:
                self.engine.running = False

    def remove_messages(self):
        # remove old messages
        messages = self.engine.logger.messages
        self.engine.logger.messages = list(filter(alive, messages))

    def process(self):
        # self.engine.logger.messages.append(
        #     Message("Graveyard", 1)
        # )
        self.remove_effects()
        self.remove_units()
        self.remove_messages()
