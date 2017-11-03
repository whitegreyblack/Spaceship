import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))+'/../')
from spaceship.constants import MENU_SCREEN_WIDTH as SCREEN_WIDTH
from spaceship.constants import MENU_SCREEN_HEIGHT as SCREEN_HEIGHT
from bearlibterminal import terminal as term
from spaceship.screen_functions import *
from spaceship.setup import setup, output, toChr, setup_font
from spaceship.maps import toInt

def new_name(character) -> (int, str):
    def text():
        term.puts(center(direction_name, xhalf*2), yhalf-5, direction_name)
        term.puts(center(direction_exit[2:], xhalf*2), yhalf+4, direction_exit)
        term.puts(center(direction_exit_program[2:], xhalf*2), yhalf+8, direction_exit_program)

    def border():
        # for k in range(SCREEN_WIDTH):
        #     term.puts(k, 3, toChr("2550"))
        #     term.puts(k, SCREEN_HEIGHT-3, toChr("2550"))
        for i in range(xhalf-fifth, xhalf+fifth):
            term.puts(i, yhalf-2, "{}".format(chr(toInt('2550'))))
            term.puts(i, yhalf, "{}".format(chr(toInt('2550'))))
            
        for j in range(yhalf-2, yhalf+1):
            term.puts(xhalf-fifth, j, "{}".format(chr(toInt('2551'))))
            term.puts(xhalf+fifth, j, "{}".format(chr(toInt('2551'))))

        term.puts(xhalf-fifth, yhalf-2, "{}".format(chr(toInt('2554'))))
        term.puts(xhalf+fifth, yhalf-2, "{}".format(chr(toInt('2557'))))
        term.puts(xhalf-fifth, yhalf, "{}".format(chr(toInt('255A'))))
        term.puts(xhalf+fifth, yhalf, "{}".format(chr(toInt('255D'))))


    direction_name = 'Enter in your name or leave blank for a random name'
    direction_exit = 'Press [[ESC]] if you wish to exit character creation'
    direction_exit_program = 'Press [[Shift]]+[[ESC]] to exit to main menu'
    xhalf = SCREEN_WIDTH//2
    yhalf = SCREEN_HEIGHT//2
    fifth = SCREEN_WIDTH//5
    # result, text = term.read_str(xhalf-fifth+1, yhalf-1, "", 30)

    string = ''
    invalid = False
    while True:
        term.clear()
        border()
        text()
        term.puts(xhalf-fifth+1, yhalf-1, string)
        if invalid:
            term.puts(
                xhalf-fifth-5, 
                yhalf+1, 
                '[c=red]{} is not a valid character for name creation[/c]'.format(
                    chr(term.state(term.TK_WCHAR))))
        term.refresh()
        invalid = False
        key = term.read()
        if key == term.TK_ESCAPE:
            if term.state(term.TK_SHIFT):
                return(output(-2, 'EXIT'))
            elif not string:
                return(output(-1, 'BACK'))
            else:
                string = string[0:len(string)-1]

        elif key == term.TK_ENTER:
            if not string:
                string = 'some random name'
            else:
                return output(0, string)
    
        elif key == term.TK_BACKSPACE:
            if string:
                string = string[0:len(string)-1]

        elif term.check(term.TK_WCHAR) and len(string) < 30:
            # make sure these characters are not included in names
            if chr(term.state(term.TK_WCHAR)) not in (
                '1234567890!@#$%^&&*()-=_+,./<>?";[]{}\|~`'):
                string += chr(term.state(term.TK_WCHAR))
            else:
                invalid = True

if __name__ == "__main__":
    term.open()
    setup_font('Ibm_cga', 8, 8)
    term.set('window: size=80x50, cellsize=auto, title="Spaceship"')    
    name = new_name(None)
    term.refresh()
