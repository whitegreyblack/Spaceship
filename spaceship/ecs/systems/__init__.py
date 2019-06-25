from .move_system import MovementSystem
from .collide_system import CollisionSystem
from .input_system import InputSystem
from .grave_system import GraveyardSystem
from .render_system import RenderSystem
from .attack_system import AttackSystem

systems = (
    AttackSystem,
    MovementSystem,
    CollisionSystem,
    InputSystem,
    GraveyardSystem,
    RenderSystem
)