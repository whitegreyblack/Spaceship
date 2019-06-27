# scene.py

"""Holds different windows"""

class Scene:
    def __init__(self, engine, terminal):
        self.engine = engine
        self.terminal = terminal

class InventoryMenu(Scene):
    def render(self):
        self.terminal.clear()
        self.terminal.border()
        self.terminal.addstr(0, 1, '[inventory]')
        self.terminal.refresh()
    
    def get_input(self):
        char = self.terminal.getch()
        self.terminal.addstr(1, 1, f"{char}")
        self.terminal.refresh()
        return False

class MainMenu(Scene):
    def __init__(self, engine):
        super().__init__(engine)
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
        char = self.terminal.getch()
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

class GameWindow(Scene):
    ...
