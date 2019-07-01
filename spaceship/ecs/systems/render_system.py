# render_system.py

"""Render system class"""

import curses
import time

from maps.map_raycast import raycast
from .system import System
from ecs.managers import join

class InventoryMenu:
    def __init__(self, engine):
        self.engine = engine
    
    def render_items(self):
        inventory = self.engine.inventories.find(self.engine.player)
        self.engine.terminal.addstr(1, 1, f"{inventory}")
        items = []
        for eid, (_, info) in join(self.engine.items, self.engine.infos):
            if eid in inventory.items:
                items.append(info)
        for i, info in enumerate(items):
            self.engine.terminal.addstr(2+i, 1, f"{i+1}. {info.name}")

    def render(self):
        self.engine.terminal.clear()
        self.engine.terminal.border()
        self.engine.terminal.addstr(0, 1, '[inventory]')

        self.render_items()

        self.engine.terminal.refresh()
    
    def get_input(self):
        char = self.engine.get_input()
        self.engine.terminal.addstr(1, 1, f"{char}")
        self.engine.terminal.refresh()
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

        self.engine.terminal.clear()
        self.engine.terminal.border()
        self.engine.terminal.addstr(0, 1, '[main_menu]')
        for i, option in enumerate(self.options):
            current_option = i == self.index
            current_index_offset = 0
            if current_option:
                current_index_offset = current_x_offset
            self.engine.terminal.addstr(
                y + option_y_offset + i,
                x + option_x_offset + current_index_offset,
                f"{'> ' if current_option else ''}{option}"
            )
        self.engine.terminal.refresh()

    def get_input(self) -> (bool, bool):
        # keep_open, exit_prog
        char = self.engine.get_input()
        self.engine.terminal.addstr(1, 1, f"{char}")
        self.engine.terminal.refresh()
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
        self.engine.terminal.addstr(y, x, string)

    def render_char(self, x, y, character, color_pair=0):
        self.engine.terminal.addch(y, x, character, color_pair)

    def render_header(self, redraw=False):
        health = self.engine.healths.find(self.engine.player)
        position = self.engine.positions.find(self.engine.player)
        self.header_x_offset = self.engine.map_x_offset
        self.header_y_offset = self.engine.map_y_offset
        self.render_string(
            self.header_x_offset,
            self.header_y_offset,
            f"{health.cur_hp}/{health.max_hp} {position.x}, {position.y}"
        )

    def render_map(self, redraw=False):
        # world = self.engine.entity.find(self.engine.map_id)
        # position = self.engine.positions.find(self.engine.player)
        # self.engine.world.do_fov(position.x, position.y, 10)
        self.map_x_offset = self.header_x_offset
        self.map_y_offset = self.header_y_offset + 1

        generator = join(
            self.engine.visibilities,
            self.engine.positions,
            self.engine.renders
        )
        for _, (visibility, position, render) in generator:
            if visibility.level > 0:
                self.render_char(
                    position.x + self.map_x_offset,
                    position.y + self.map_y_offset,
                    render.char,
                    curses.color_pair(visibility.level)
                )
        if redraw:
            self.redraw()

    def render_fov(self):
        raycast(self.engine)

    def render_units(self, redraw=True):
        units = join(
            self.engine.healths,
            self.engine.positions, 
            self.engine.renders,
            self.engine.visibilities
        )
        tiles = join(
            self.engine.positions,
            self.engine.visibilities
        )
        for eid, (health, position, render, visibility) in units:
            if visibility.level > 1:
                self.render_char(
                    position.x + self.map_x_offset,
                    position.y + self.map_y_offset,
                    render.char,
                    curses.color_pair(visibility.level)
                )
        if redraw:
            self.redraw()

    def render_items(self, redraw=True):
        g = join(
            self.engine.items,
            self.engine.positions,
            self.engine.renders,
            self.engine.visibilities
        )
        for eid, (item, position, render, visibility) in g:
            if visibility.level > 1:
                self.render_char(
                    position.x + self.map_x_offset,
                    position.y + self.map_y_offset,
                    render.char,
                    curses.color_pair(visibility.level)
                )

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
        for eid, effect in self.engine.effects:
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

    def render_log(self, log, ly, lx, redraw=True):
        self.engine.terminal.addstr(ly, lx, log.string)
        log.lifetime -= 1

    def render_logs(self, redraw=True):
        logs = filter(lambda x: x.lifetime > 0, self.engine.logger.messages)
        tilemap = self.engine.tilemaps.find(self.engine.world)
        # print(list(logs))
        for y, log in enumerate(logs):
            # stop if lines reach end of the line 
            # could also index messages by height of window
            log_y = self.map_y_offset + tilemap.height + y
            if log_y > self.engine.height - 2:
                # print(log_y, self.engine.height - 2, log_y>self.engine.height-2)
                break
            self.render_log(log, log_y, self.map_x_offset, redraw)
        if redraw:
            self.engine.terminal.refresh()

    def redraw(self):
        self.engine.terminal.refresh()

    def process(self):
        self.engine.terminal.erase()
        self.engine.terminal.border()

        self.render_header(False)
        self.render_map(False)
        # self.render_effects(True)
        self.render_items(False)
        self.render_units(False)

        self.render_logs(False)
        self.redraw()
