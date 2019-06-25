# common.py

"""Holds commonly used simple data class objects"""

from dataclasses import dataclass, field
from classes.utils import dimensions


@dataclass
class Event:
    ...

@dataclass
class CollisionEvent(Event):
    collider: int
    collidee: int = -1
    x: int = 0
    y: int = 0

@dataclass
class Message:
    string: str
    lifetime: int = 1

@dataclass
class Logger:
    world: str = None
    header: str = ""
    messages: list = field(default_factory=list)
    def add(self, message, lifetime=1):
        self.messages.append(Message(message, lifetime))

@dataclass
class Map:
    array: list
    width: int
    height: int
    def characters(self):
        for j in range(self.height):
            for i in range(self.width):
                yield i, j, self.array[j][i]
    def spaces(self):
        for j in range(self.height):
            for i in range(self.width):
                if self.array[j][i] == '.':
                    yield i, j
    def is_door(self, i, j):
        return self.array[j][i] in ('+', '/')
    def open_door(self, i, j):
        if self.array[j][i] == '+':
            self.array[j][i] = '/'
        return self.array[j][i] == '/'
    def close_door(self, i, j):
        if self.array[j][i] == '/':
            self.array[j][i] = '+'
        return self.array[j][i] == '+'
    def is_blocked(self, i, j):
        return self.array[j][i] in ('#', '+')
    @classmethod
    def factory(cls, string):
        return cls(*dimensions(string))

@dataclass
class LightMap:
    array: list
    width: int
    height: int

def render_main_menu(engine):
    engine.screen.clear()
    engine.screen.border()

    index = 0
    options = ['back', 'save', 'quit']

    # title
    engine.screen.addstr(0, 1, '[main_menu]')
    
    x = engine.width // 2
    y = engine.height // 2
    
    option_y_offset = - 1
    option_x_offset = - (max(map(len, options)) // 2)
    current_x_offset = -2

    while True:
        engine.screen.clear()
        for i, option in enumerate(options):
            engine.screen.addstr(
                y + option_y_offset + i,
                x + option_x_offset + (current_x_offset if i == index else 0),
                f"{'> ' if i == index else ''}{option}"
            )
        engine.screen.refresh()
        char = engine.screen.getch()
        if char == ord('q') or (char == 10 and options[index] == 'quit'):
            engine.running = False
            curses.endwin()
            break
        elif char == 27:
            break
        elif char == 258:
            index = (index + 1) % len(options)
        elif char == 259:
            index = (index - 1) % len(options)
    return True

def direction_from_input(engine):
    curses.flushinp()
    char = engine.get_input()
    # check exit input
    if char == ord('q'):
        engine.running = False
        return None, None, None
    # check inventory command
    engine.logger.add(
        f"{char}, {repr(char)}, {chr(char)}"
    )
    print(f"{char}, {repr(char)}, {chr(char)}")
    command = engine.keyboard.get(char, None)
    if not command:
        engine.logger.add("Command unknown")
    return command

def direction_from_random(engine, entity):
    position = engine.position_manager.find(entity)
    possible_spaces = []
    for x, y in nine_square():
        if not 0 <= position.x + x < engine.world.width:
            continue
        if not 0 <= position.y + y < engine.world.height:
            continue
        cell = engine.world.array[position.y+y][position.x+x]
        if cell not in ('#', '+'):
            possible_spaces.append((x, y))
    index = random.randint(0, len(possible_spaces)-1)
    return possible_spaces[index]
