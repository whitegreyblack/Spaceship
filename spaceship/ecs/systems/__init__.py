from .move_system import MovementSystem
from .collide_system import CollisionSystem
from .input_system import InputSystem
from .grave_system import GraveyardSystem
from .render_system import RenderSystem

systems = (
    MovementSystem,
    CollisionSystem,
    InputSystem,
    GraveyardSystem,
    RenderSystem
)