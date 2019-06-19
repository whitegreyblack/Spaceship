# grave_system

"""Graveyard system class"""

from .system import System


alive = lambda message: message.lifetime > 0

class GraveyardSystem(System):
    def process(self):
        # remove old messages
        messages = self.engine.logger.messages
        self.engine.logger.messages = list(filter(alive, messages))

"""
# from old code...
def graveyard_system(logger, managers):
    entities_to_remove = []
    for entity_id, health in managers['health'].components.items():
        entity = managers['entity'].find(entity_id)
        info = managers['information'].find(entity)
        if health.cur_hp < 1:
            entities_to_remove.append(entity)
            ai = managers['ai'].find(entity)
    for entity in entities_to_remove:
        for manager in managers.values():
            manager.remove(entity)
"""