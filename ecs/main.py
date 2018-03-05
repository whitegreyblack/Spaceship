from bearlibterminal import terminal as term

class Graph:
    pass

class Node:
    pass

class Scene:
    connections = dict()
    def __init__(self, screen, connections: dict = None):
        self.screen = screen
        self.current_screen = screen
        self.index = 0
        if connections:
            self.connections.update(connections)
        self.run()

    def run(self) -> None:
        self.proceed = True
        while True:
            # screen is only draw functions -- no logic
            term.clear()
            self.current_screen()
            term.refresh()
            self.handle_input()
            if not self.proceed:
                exit()
        self.proceed = True

    def handle_input(self) -> None:
        userin = term.read()
        while userin in (term.TK_SHIFT, term.TK_ALT, term.TK_CONTROL):
            term.puts(0, 0, 'Not a valid command')
            userin = term.read()
        if userin in (term.TK_ESCAPE,):
            self.proceed = False
            return False
        for key, (screen, connections) in self.connections.items():
            if userin == key:
                self.current_screen = screen
                self.connections = connections

def dimensions() -> (int, int):
    return term.state(term.TK_WIDTH), term.state(term.TK_HEIGHT)

def calc_options_heights(height: int, header: int, footer: int) -> list:
    '''Returns the height values for the options based on screen height'''
    def calculate(option: int) -> int:
        half_height = total_height // 2
        quarter_height = total_height // 4
        return header + half_height - quarter_height + option
    total_height = height - header - footer
    return [calculate(option * 2) for option in range(4)]

def center(text: str, width: int) -> int:
    '''Returns x position for string given a width length'''
    if isinstance(text, str):
        text = len(text)
    return width // 2 - text // 2

def main_screen() -> None:
    main_title = "ECS SYSTEM"
    x, y = dimensions()
    xo, yo = center(main_title, x), y // 3
    options = ['play game', 'exit']
    heights = calc_options_heights(y, yo, y - 1)
    term.puts(xo, yo, main_title)
    for opt, heights in zip(options, heights):
        term.puts(xo + 2, yo + heights, opt)

def make_screen() -> None:
    main_title = "Make Screen"
    x, y = dimensions()
    xo, yo = center(main_title, x), y // 3
    term.puts(xo, yo, main_title)

if __name__ == "__main__":
    term.open()
    s = Scene(main_screen, connections={
        term.TK_P: (make_screen, {}),
        term.TK_Q: (exit, {})
    })
