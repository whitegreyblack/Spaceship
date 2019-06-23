# render_system.py

"""Render system class"""

import time

from .system import System


class RenderSystem(System):
    def render_string(self, x, y, string):
        self.engine.screen.addstr(y, x, string)

    def render_char(self, x, y, character):
        self.engine.screen.addch(y, x, character)

    def render_header(self, redraw=False):
        health = self.engine.health_manager.find(self.engine.player)
        position = self.engine.position_manager.find(self.engine.player)
        self.header_x_offset = self.engine.map_x_offset
        self.header_y_offset = self.engine.map_y_offset
        self.render_string(
            self.header_x_offset,
            self.header_y_offset,
            f"{health.cur_hp}/{health.max_hp} {position.x}, {position.y}"
        )

    def render_map(self, redraw=False):
        self.map_x_offset = self.header_x_offset
        self.map_y_offset = self.header_y_offset + 1
        for x, y, c in self.engine.world.characters():
            self.render_char(
                x + self.map_x_offset, 
                y + self.map_y_offset, 
                c
            )
        if redraw:
            self.redraw()

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
            self.render_char(
                position.x + self.map_x_offset,
                position.y + self.map_y_offset,
                render.char
            )
        if redraw:
            self.redraw()

    # def render_items(self, redraw=True):
    #     position_manager = self.engine.position_manager
    #     for eid, position in position_manager.components.items():
    #         entity = self.engine.entity_manager.find(eid)
    #         if not entity or position.:
    #             continue
    #         render = self.engine.render_manger.find(entity)

    def render_effect(self, x, y, effect, redraw=True):
        self.render_char(
            x + self.map_x_offset,
            y + self.map_y_offset,
            effect.char
        )
        if redraw:
            self.redraw()
            time.sleep(.1)

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

    def render_logs(self, redraw=True):
        for y, log in enumerate(self.engine.logger.messages):
            # stop if lines reach end of the line 
            # could also index messages by height of window
            if map_offset_y + y > self.engine.height - 2:
                break
            self.engine.screen.addstr(
                self.map_y_offset + self.engine.world.height + y, 
                self.map_x_offset, 
                log.string
            )
            log.lifetime -= 1

    def redraw(self):
        self.engine.screen.refresh()

    def process(self):
        self.engine.screen.erase()
        self.engine.screen.border()

        self.render_header(False)
        self.render_map(False)
        self.render_effects(True)
        # self.render_items(False)
        self.render_units(False)

        self.render_logs(False)
        self.redraw()
