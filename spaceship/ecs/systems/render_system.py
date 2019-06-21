# render_system.py

"""Render system class"""

import time

from ..common import Message
from .system import System

redraw = 0

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

    def render_effect(self, x, y, effect, redraw=True):
        self.engine.screen.addch(
            y + self.engine.map_y_offset,
            x + self.engine.map_x_offset,
            effect.char
        )
        if redraw:
            self.redraw()
            time.sleep(.05)

    def render_effects(self, redraw=True):
        effect_manager = self.engine.effect_manager
        for eid, effect in effect_manager.components.items():
            if effect.ticks > 0:
                entity = self.engine.entity_manager.find(eid)
                position = self.engine.position_manager.find(entity)
                movement = self.engine.movement_manager.find(entity)
                x, y = position.x, position.y
                if movement:
                    x, y = x + movement.x, y + movement.y
                self.render_effect(x, y, effect, False)
                effect.ticks -= 1
            if redraw:
                self.redraw()
                time.sleep(1)

    def redraw(self):
        global redraw
        redraw += 1
        self.engine.screen.refresh()
        print(redraw)

    def process(self):
        self.engine.screen.erase()
        self.engine.screen.border()

        self.render_map(False)
        self.render_effects(True)
        self.render_units(False)

        map_offset_y = self.engine.map_y_offset
        map_offset_x = self.engine.world.width + self.engine.map_x_offset + 2

        # logs
        for y, log in enumerate(self.engine.logger.messages):
            # stop if lines reach end of the line 
            # could also index messages by height of window
            if map_offset_y + y > self.engine.height - 2:
                break
            self.engine.screen.addstr(
                map_offset_y + y, 
                map_offset_x, 
                log.string
            )
            log.lifetime -= 1
        self.redraw()
