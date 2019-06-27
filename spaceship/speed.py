# curses_speed.py

"""Try running a main loop with no blocking input ran at 60 fps"""

import curses
import time
import os

def test(screen):
    curses.curs_set(0)
    # screen.nodelay(1)
    curses.halfdelay(1)
    
    fps_target = 60
    fps_render_time = 1000000000 / fps_target
    fps_update_time = time.time()
    fps_counter = fps_value = 0

    render_time = fps_update_time

    keypress = ""
    keypress_counter = 0

    position = 1
    
    height, width = screen.getmaxyx()

    proceed = True
    while proceed:
        screen.erase()
        screen.border()
        screen.addstr(0, 1, '[speed]')
        screen.addstr(1, 1, f"fps: {fps_value}")
        screen.addstr(2, 1, f"keypress: {keypress} {f'x{keypress_counter}' if keypress_counter else ''}")
        screen.addstr(3, 1, f"{fps_render_time}")
        screen.addstr(5, position, f"@")

        fps_counter += 1
        position = (position + 1) % (width - 2) + 1
        tm = time.time()

        if tm > fps_update_time + 1:
            fps_value = fps_counter
            fps_counter = 0
            fps_update_time = tm
            fps_render_time = (tm - fps_update_time) * 100000000000

        char = screen.getch()
        if char == ord('q'):
            print(char)
            proceed = False
        if 97 <= char < 97 + 26 + 1:
            if keypress == chr(char):
                keypress_counter += 1
            else:
                keypress = chr(char)
                keypress_counter = 0

if __name__ == "__main__":
    curses.wrapper(test)

