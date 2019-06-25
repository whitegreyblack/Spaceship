# attack_system.py

"""Attack system class"""

import time

from ecs import Destroy, Effect

from .system import System


class AttackSystem(System):
    def process(self, entity, other):
        ...
