# Move_system.py

"""Movement system class"""

import time

from ecs import Collision, Movement

from .system import System


class MovementSystem(System):
    def move(self, position, x, y):
        position.x += x
        position.y += y

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
                    # continue
                    return False

            # not blocked by units
            # unit_blocked = False
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
                    # return False
                    return self.engine.collision_system.process()
                    # self.engine.logger.messages.append(
                    #     Message("Unit hits another", 1

                    #     )
                    # )
                    # x, y = entity_movement.x, entity_movement.y
                    # direction = utils.direction[(x, y)]
                    # message = utils.messages['blocked'].format(direction)
                    # logger.messages.append(Message(message, 1))
                    # unit_blocked = True
                    # break
            
            # if not unit_blocked:
            self.move(entity_position, entity_movement)
        movement_manager.components.clear()
        return True

    def process_movement(self, entity):
        position = self.engine.position_manager.find(entity)
        movement = self.engine.movement_manager.find(entity)

        x = position.x + movement.x
        y = position.y + movement.y

        # print(entity.id, 'new position', x, y)
        if self.engine.world.array[y][x] in ('#', '+'):
            # print('position blocked by wall')
            # if entity == self.engine.player:
            #     self.engine.logger.add('new position blocked by environment')
            self.engine.collision_manager.add(entity, Collision(x=x, y=y))
            return self.engine.collision_system.process_collision(entity)
        positions = self.engine.position_manager.components.items()
        for eid, p in positions:
            if eid not in self.engine.entity_manager.ids:
                continue
            other_entity = entity.id != eid
            same_position = (p.x, p.y) == (x, y)
            if other_entity and same_position and p.blocks_movement:
                # print('new position blocked by unit', eid)
                self.engine.collision_manager.add(entity, Collision(eid))
                return self.engine.collision_system.process_collision(entity)
        self.move(position, movement)
        # self.engine.logger.add(f"{entity.id} moves {'left' if movement.x < 0 else 'right'}")
        return True

    def process(self, movement):
        entity, position, movement = movement
        x, y = position.x + movement[0], position.y + movement[1]
        if self.engine.world.world[y][x] in ('#', '+'):
            self.engine.logger.add(f"collision with environment")
            return  
        for other_id, other_position in self.engine.position.components.items():
            if other_id == entity.id:
                continue
            future_position_blocked = (
                (x, y) == (other_position.x, other_position.y)
            )
            if future_position_blocked:
                self.engine.add_component(entity, 'collision', other_id)
                self.engine.logger.add(f"collision")
                return
        self.move(position, *movement)
