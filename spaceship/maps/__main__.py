# __main__.py

"""Runs the package as an application when running as module"""

import curses
from collections import namedtuple

import click

from ecs import Position
from keyboard import keyboard

from . import BltMap, Map, RayCastedMap, dungeons

directions = {
    'down': (0, 1),
    'up': (0, -1),
    'left': (-1, 0),
    'right': (1, 0)
}

def example(screen, m):
    """
    Initializes map and character objects then calls a do while loop to
    run the game.
    """
    # turn off cursor
    curses.curs_set(0)

    # define some variables
    position = namedtuple("Position", "x y")
    player = position(m.width//2, m.height//2)

    while True:
        # clear screen
        screen.erase()
        # calculates fov
        m.do_fov(*player, 25)
        # adds character for every square character can see
        for x, y, c, _ in m.lighted_tiles:
            # limit map rendering if larger than regular terminal size
            if x > 79 or y > 24:
                continue
            # adds character
            screen.addch(y, x, c)
        # add player
        screen.addch(player.y, player.x, '@')
        screen.refresh()

        # keypress and movements
        keypress = keyboard[screen.getch()]
        if keypress in ('keypress', 'q'):
            break
        move = directions.get(keypress, None)
        if move:
            future_position = position(*(sum(p) for p in zip(player, move)))
            if not m.is_blocked(future_position.x, future_position.y):
                player = future_position
        screen.addstr(23, 0, keypress)

def main(screen, mapclass, dungeon):
    dungeon = dungeons.get(dungeon.lower(), 'dungeon')
    if mapclass == 'blt':
        world = BltMap(dungeon)
    elif mapclass == 'ray':
        world = RayCastedMap(dungeon)
    else:
        world = Map(dungeon)
    example(screen, world)

@click.command()
@click.option('-m', '--mapclass', default='map')
@click.option('-d', '--dungeon', default='dungeon')
def preload(mapclass, dungeon):
    curses.wrapper(main, mapclass, dungeon)

if __name__ == "__main__":
    preload()
