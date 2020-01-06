# turn_system.py

"""Turn system"""

import curses
import random
import time
from dataclasses import dataclass, field

from spaceship.ecs import Movement, Position
from spaceship.space import eight_square, nine_square

from .system import System

class TurnSystem(System):
    def process(self):
        for entity in self.engine.entities:
            needs_input = self.engine.input.find(entity)
            print(entity, needs_input)
            if not needs_input:
                # found an entity that doesn't require an action
                continue
            print(f"Entity={entity}")

        for entity, needs_input in self.engine.input:
            print(entity, needs_input)
