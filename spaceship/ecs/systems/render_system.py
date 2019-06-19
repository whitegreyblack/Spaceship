# render_system.py

"""Render system class"""

from .system import System


class RenderSystem(System):
    def render_map(self):
        chars = {}
        for eid, position in self.engine.position_manager.components.items():
            entity = self.engine.entity_manager.find(eid)
            render = self.engine.render_manager.find(entity)
            if not render:
                continue
            chars[(position.x, position.y)] = render.char
        for x, y, c in self.engine.world.characters():
            if (x, y) in chars:
                yield x, y, chars[(x, y)]
            else:
                yield x, y, c

    def process(self):
        self.engine.screen.clear()
        self.engine.screen.border()

        # map
        for x, y, c in self.render_map():
            self.engine.screen.addch(
                y + self.engine.map_y_offset, 
                x + self.engine.map_x_offset, 
                c
            )

        map_offset = y + self.engine.map_y_offset + 1

        # logs
        for height, log in enumerate(self.engine.logger.messages):
            self.engine.screen.addstr(map_offset, 0, log.string)
            log.lifetime -= 1
        self.engine.screen.refresh()
