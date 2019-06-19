# Move_system.py

"""Movement system class"""

from ..common import Message
from .system import System


class MovementSystem(System):
    def move(self, position, movement):
        position.x += movement.x
        position.y += movement.y

    def process(self):
        entity_manager = self.engine.entity_manager
        movement_manager = self.engine.movement_manager
        position_manager = self.engine.position_manager
        ai_manager = self.engine.ai_manager
        for entity_id, entity_movement in movement_manager.components.items():
            entity = self.engine.entity_manager.find(entity_id)
            entity_position = position_manager.find(entity)
            entity_ai = ai_manager.find(entity)
            x = entity_position.x + entity_movement.x
            y = entity_position.y + entity_movement.y

            # not blocked by environment
            if self.engine.world.array[y][x] in ('#', '+'):
                if not entity_ai:
                    continue 

            # not blocked by units
            unit_blocked = False
            for other_id, other_position in position_manager.components.items():
                if other_id == entity.id:
                    continue
                # NOTE: should be using the future positions of other units. 
                #     : Maybe create a local position manager to compare future position to?
                future_position_blocked = (
                    (x, y) == (other_position.x, other_position.y)
                )
                if future_position_blocked:
                    self.engine.add_component(entity, 'collision', other_id)

                    self.engine.logger.messages.append(
                        Message("Unit hits another", 1

                        )
                    )
                    # x, y = entity_movement.x, entity_movement.y
                    # direction = utils.direction[(x, y)]
                    # message = utils.messages['blocked'].format(direction)
                    # logger.messages.append(Message(message, 1))
                    unit_blocked = True
                    break
            
            if not unit_blocked:
                self.move(entity_position, entity_movement)
        movement_manager.components.clear()
