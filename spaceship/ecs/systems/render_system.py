# render_system.py

"""Render system class"""

import curses
import time

from .system import System


class InventoryMenu:
    def __init__(self, engine):
        self.engine = engine
    
    def render(self):
        self.engine.screen.clear()
        self.engine.screen.border()
        self.engine.screen.addstr(0, 1, '[inventory]')
        self.engine.screen.refresh()
    
    def get_input(self):
        char = self.engine.get_input()
        self.engine.screen.addstr(1, 1, f"{char}")
        self.engine.screen.refresh()
        return False

class MainMenu:
    def __init__(self, engine):
        self.engine = engine
        self.index = 0
        self.options = ['back', 'save', 'quit']
    
    def render(self):
        x = self.engine.width // 2
        y = self.engine.height // 2
        
        option_y_offset = - 1
        option_x_offset = - (max(map(len, self.options)) // 2)
        current_x_offset = -2

        self.engine.screen.clear()
        self.engine.screen.border()
        self.engine.screen.addstr(0, 1, '[main_menu]')
        for i, option in enumerate(self.options):
            current_option = i == self.index
            current_index_offset = 0
            if current_option:
                current_index_offset = current_x_offset
            self.engine.screen.addstr(
                y + option_y_offset + i,
                x + option_x_offset + current_index_offset,
                f"{'> ' if current_option else ''}{option}"
            )
        self.engine.screen.refresh()

    def get_input(self) -> (bool, bool):
        # keep_open, exit_prog
        char = self.engine.get_input()
        self.engine.screen.addstr(1, 1, f"{char}")
        self.engine.screen.refresh()
        q_keypress = char == ord('q')
        quit_select = char == 10 and self.options[self.index] == 'quit'
        back_select = char == 10 and self.options[self.index] == 'back'
        if q_keypress or quit_select:
            self.engine.running = False
            return False
        elif char == 27 or back_select:
            return False
        elif char == 258:
            self.index = (self.index + 1) % len(self.options)
            return True
        elif char == 259:
            self.index = (self.index - 1) % len(self.options) 
            return True
        else:
            return self.get_input()

class RenderSystem(System):
    def __init__(self, engine):
        super().__init__(engine)
        self.main_menu = MainMenu(engine) 
        self.inventory_menu = InventoryMenu(engine)

    def render_main_menu(self):
        self.main_menu.render()

    def render_string(self, x, y, string):
        self.engine.screen.addstr(y, x, string)

    def render_char(self, x, y, character, color_pair=0):
        self.engine.screen.addch(y, x, character, color_pair)

    def render_header(self, redraw=False):
        health = self.engine.health.find(self.engine.player)
        position = self.engine.position.find(self.engine.player)
        self.header_x_offset = self.engine.map_x_offset
        self.header_y_offset = self.engine.map_y_offset
        self.render_string(
            self.header_x_offset,
            self.header_y_offset,
            f"{health.cur_hp}/{health.max_hp} {position.x}, {position.y}"
        )

    def render_map(self, redraw=False):
        position = self.engine.position.find(self.engine.player)
        self.engine.world.do_fov(position.x, position.y, 10)
        self.map_x_offset = self.header_x_offset
        self.map_y_offset = self.header_y_offset + 1
        for x, y, c, l in self.engine.world.lighted_tiles:
            self.render_char(
                x + self.map_x_offset,
                y + self.map_y_offset,
                c,
                curses.color_pair(l)
            )
        if redraw:
            self.redraw()

    def render_units(self, redraw=True):
        position = self.engine.position
        for eid, position in position.components.items():
            entity = self.engine.entities.find(eid)
            if not entity:
                continue
            render = self.engine.render.find(entity)
            health = self.engine.health.find(entity)
            if not render or (health and health.cur_hp < 1):
                continue
            l = self.engine.world.lit(position.x, position.y)
            if l == 2:
                self.render_char(
                    position.x + self.map_x_offset,
                    position.y + self.map_y_offset,
                    render.char,
                    curses.color_pair(l)
                )
        if redraw:
            self.redraw()

    # def render_items(self, redraw=True):
    #     position = self.engine.position
    #     for eid, position in position.components.items():
    #         entity = self.engine.entities.find(eid)
    #         if not entity or position.:
    #             continue
    #         render = self.engine.render_manger.find(entity)

    def render_effect(self, x, y, effect, redraw=True):
        self.render_char(
            x + self.map_x_offset,
            y + self.map_y_offset,
            effect.char,
            curses.color_pair(1)
        )
        if redraw:
            self.redraw()
            time.sleep(.1)

    def render_effects(self, redraw=True):
        effect = self.engine.effect
        for eid, effect in effect.components.items():
            if effect.ticks > 0:
                entity = self.engine.entities.find(eid)
                position = self.engine.position.find(entity)
                movement = self.engine.movement.find(entity)
                x, y = position.x, position.y
                if movement:
                    x, y = x + movement.x, y + movement.y
                self.render_effect(x, y, effect, False)
                effect.ticks -= 1
            if redraw:
                self.redraw()
                time.sleep(1)

    def render_logs(self, redraw=True):
        logs = filter(lambda x: x.lifetime > 0, self.engine.logger.messages)
        for y, log in enumerate(logs):
            # stop if lines reach end of the line 
            # could also index messages by height of window
            log_y = self.map_y_offset + self.engine.world.height + y
            if log_y > self.engine.height - 2:
                break
            self.engine.screen.addstr(
                log_y,
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
