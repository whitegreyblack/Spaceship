# render_system.py

"""Render system class"""

import curses
import time

from maps.map_raycast import raycast
from .system import System
from ecs.managers import join

def border(screen: object, x: int, y: int, dx: int, dy: int) -> None:
    """
    Draws a box with given input parameters using the default characters
    """
    screen.vline(y, x, curses.ACS_SBSB, dy)
    screen.vline(y, x + dx - 1, curses.ACS_SBSB, dy)
    screen.hline(y, x, curses.ACS_BSBS, dx)
    screen.hline(y + dy - 1, x, curses.ACS_BSBS, dx)
    screen.addch(y, x, curses.ACS_BSSB)
    screen.addch(y, x + dx - 1, curses.ACS_BBSS)
    screen.addch(y + dy - 1, x, curses.ACS_SSBB)
    screen.addch(y + dy - 1, x + dx - 1, curses.ACS_SBBS)

class InventoryMenu:
    def __init__(self, engine, terminal):
        self.engine = engine
        self.terminal = terminal
    
    def render_items(self):
        inventory = self.engine.inventories.find(self.engine.player)
        self.terminal.addstr(1, 1, f"{inventory}")
        items = []
        for eid, (_, info) in join(self.engine.items, self.engine.infos):
            if eid in inventory.items:
                items.append(info)
        for i, info in enumerate(items):
            self.terminal.addstr(2+i, 1, f"{i+1}. {info.name}")

    def render(self):
        self.terminal.clear()
        self.terminal.border()
        self.terminal.addstr(0, 1, '[inventory]')

        self.render_items()

        self.terminal.refresh()
    
    def get_input(self):
        char = self.engine.get_input()
        self.terminal.addstr(1, 1, f"{char}")
        self.terminal.refresh()
        return False

class MainMenu:
    def __init__(self, engine, terminal):
        self.engine = engine
        self.terminal = terminal
        self.index = 0
        self.options = ['back', 'save', 'quit']
    
    def render(self):
        x = self.engine.width // 2
        y = self.engine.height // 2
        
        option_y_offset = - 1
        option_x_offset = - (max(map(len, self.options)) // 2)
        current_x_offset = -2
 
        self.terminal.clear()
        self.terminal.border()
        self.terminal.addstr(0, 1, '[main_menu]')
        for i, option in enumerate(self.options):
            current_option = i == self.index
            current_index_offset = 0
            if current_option:
                current_index_offset = current_x_offset
            self.terminal.addstr(
                y + option_y_offset + i,
                x + option_x_offset + current_index_offset,
                f"{'> ' if current_option else ''}{option}"
            )
        self.terminal.refresh()

    def get_input(self) -> (bool, bool):
        # keep_open, exit_prog
        char = self.engine.get_input()
        self.terminal.addstr(1, 1, f"{char}")
        self.terminal.refresh()
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
    def __init__(self, engine, terminal, logger=None):
        super().__init__(engine, logger)
        self.terminal = terminal
        self.main_menu = MainMenu(engine, terminal) 
        self.inventory_menu = InventoryMenu(engine, terminal)

        self.height, self.width = terminal.getmaxyx()

        self.inventory_x = 1
        self.inventory_y = 1
        self.inventory_width = 14
        self.inventory_height = 24

        self.header_x = self.inventory_x + self.inventory_width
        self.header_y = 1
        self.header_width = 80
        self.header_height = 1

        # maximum bounds for map size; any larger and scroll is enabled
        self.map_x = self.inventory_x + self.inventory_width
        self.map_y = self.header_y + self.header_height
        self.map_width = 80
        self.map_height = 25

        self.enemies_list_x = self.map_x + self.map_width + 1
        self.enemies_list_y = 1
        self.enemies_list_width = 20
        self.enemies_list_height = 24

        self.logs_x = self.inventory_x + self.inventory_width
        self.logs_y = self.map_y + self.map_height

    def render_main_menu(self):
        self.main_menu.render()

    def render_string(self, x, y, string):
        self.terminal.addstr(y, x, string)

    def render_char(self, x, y, character, color_pair=0):
        self.terminal.addch(y, x, character, color_pair)

    def render_fov(self):
        raycast(self.engine)

    def render_inventory(self, redraw=False):
        border(
            self.terminal, 
            self.inventory_x, 
            self.inventory_y, 
            self.inventory_width, 
            self.inventory_height
        )
        self.terminal.addstr(1, 2, '[inventory]')

        inventory = self.engine.inventories.find(self.engine.player)
        # self.terminal.addstr(1, 1, f"{inventory}")
        if not inventory.items:
            self.terminal.addstr(2, 2, 'empty')
        else:
            items = []
            for eid, (_, info) in join(self.engine.items, self.engine.infos):
                if eid in inventory.items:
                    items.append(info)
            for i, info in enumerate(items):
                self.render_string(
                    self.inventory_x + 1, 
                    self.inventory_y + 1 + i, 
                    f"{i+1}. {info.name}"
                )

    def render_header(self, redraw=False):
        health = self.engine.healths.find(self.engine.player)
        position = self.engine.positions.find(self.engine.player)
        header = f"{health.cur_hp}/{health.max_hp} {position.x}, {position.y}"
        self.render_string(self.header_x, self.header_y, header)

    def render_map(self, redraw=False):
        generator = join(
            self.engine.visibilities,
            self.engine.positions,
            self.engine.renders
        )
        for _, (visibility, position, render) in generator:
            if visibility.level > 0:
                self.render_char(
                    position.x + self.map_x,
                    position.y + self.map_y,
                    render.char,
                    curses.color_pair(visibility.level)
                )
        if redraw:
            self.redraw()

    def render_enemy(self, y, render, info, health):
        enemy = f"{render.char} {info.name} {health.cur_hp}/{health.max_hp}"
        self.render_string(
            self.enemies_list_x + 1,
            self.enemies_list_y + y + 1,
            enemy[:self.enemies_list_width-1]
        )

    def render_enemy_list(self, redraw=False):
        border(
            self.terminal, 
            self.enemies_list_x,
            self.enemies_list_y, 
            self.enemies_list_width, 
            self.enemies_list_height
        )
        self.render_string(
            self.enemies_list_x + 1,
            self.enemies_list_y,
            '[enemies]'
        )

    def render_units(self, redraw=True):
        units = join(
            self.engine.healths,
            self.engine.positions, 
            self.engine.renders,
            self.engine.infos
        )
        # look for all positions not in tile positions and visibilities
        # if their positions match and map is visible then show the unit
        enemy_count = 0
        for eid, (health, u_position, render, info) in units:
            tiles = join(self.engine.positions, self.engine.visibilities)
            for tid, (t_position, visibility) in tiles:
                if u_position == t_position and visibility.level > 1:
                    self.render_char(
                        self.map_x + u_position.x,
                        self.map_y + u_position.y,
                        render.char,
                        curses.color_pair(visibility.level)
                    )
                    if eid != self.engine.player.id:
                        self.render_enemy(
                            enemy_count,
                            render,
                            info,
                            health
                        )
                        enemy_count += 1
                    break

        if redraw:
            self.redraw()

    def render_items(self, redraw=True):
        items = join(
            self.engine.items,
            self.engine.positions,
            self.engine.renders,
        )
        for eid, (item, i_position, render) in items:
            tiles = join(self.engine.positions, self.engine.visibilities)
            for tid, (t_position, visibility) in tiles:
                if i_position == t_position and visibility.level > 1:
                    self.render_char(
                        self.map_x + i_position.x,
                        self.map_y + i_position.y,
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
        self.terminal.addstr(ly, lx, log.string)
        log.lifetime -= 1

    def render_logs(self, redraw=True):
        logs = filter(lambda x: x.lifetime > 0, self.engine.logger.messages)
        tilemap = self.engine.tilemaps.find(self.engine.world)
        # print(list(logs))
        for y, log in enumerate(logs):
            # stop if lines reach end of the line 
            # could also index messages by height of window
            log_y = self.logs_y + y
            if log_y > self.engine.height - 2:
                break
            self.render_log(log, log_y, self.logs_x, redraw)
        if redraw:
            self.terminal.refresh()

    def redraw(self):
        self.terminal.refresh()

    def process(self):
        self.terminal.erase()
        self.terminal.border()

        self.render_inventory(False)
        self.render_header(False)

        self.render_map(False)
        self.render_enemy_list(False)

        # self.render_effects(True)
        self.render_items(False)
        self.render_units(False)

        self.render_logs(False)
        self.redraw()
