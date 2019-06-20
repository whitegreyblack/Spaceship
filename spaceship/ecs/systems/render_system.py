# render_system.py

"""Render system class"""

import time

from ..common import Message
from .system import System


class RenderSystem(System):
    def render_map(self, redraw=False):
        for x, y, c in self.engine.world.characters():
            self.engine.screen.addch(
                y + self.engine.map_y_offset, 
                x + self.engine.map_x_offset, 
                c
            )
        if redraw:
            self.redraw()

    def render_unit(self, position, render):
        self.engine.screen.addch(
            position.y + self.engine.map_y_offset, 
            position.x + self.engine.map_x_offset, 
            render.char
        )

    def render_units(self, redraw=True):
        position_manager = self.engine.position_manager
        for eid, position in position_manager.components.items():
            entity = self.engine.entity_manager.find(eid)
            if not entity:
                continue
            render = self.engine.render_manager.find(entity)
            health = self.engine.health_manager.find(entity)
            if not render or (health and health.cur_hp < 1):
                continue
            self.render_unit(position, render)
        if redraw:
            self.redraw()

    def render_effect(self, position, effect, redraw=True):
        self.engine.screen.addch(
            position.y + self.engine.map_y_offset,
            position.x + self.engine.map_x_offset,
            effect.char
        )
        if redraw:
            self.redraw()

    def render_effects(self, redraw=True):
        effect_manager = self.engine.effect_manager
        for eid, effect in effect_manager.components.items():
            entity = self.engine.entity_manager.find(eid)
            position = self.engine.position_manager.find(entity)
            self.render_effect(position, effect, False)
            effect.ticks -= 1
        if redraw:
            self.redraw()

    def redraw(self):
        self.engine.screen.refresh()

    def process(self):
        self.engine.screen.clear()
        self.engine.screen.border()

        self.render_map(False)
        
        effects = self.engine.effect_manager.components.values()
        while any(e.ticks > 0 for e in effects):
            self.render_units(False)
            self.render_effects(True)
            time.sleep(0.1)

        self.render_units(False)

        map_offset_y = self.engine.map_y_offset
        map_offset_x = self.engine.world.width + self.engine.map_x_offset + 2

        # logs
        for y, log in enumerate(self.engine.logger.messages):
            # stop if lines reach end of the line 
            # could also index messages by height of window
            if map_offset_y + y > self.engine.world.height - 2:
                break
            self.engine.screen.addstr(
                map_offset_y + y, 
                map_offset_x, 
                log.string
            )
            log.lifetime -= 1
        self.redraw()
