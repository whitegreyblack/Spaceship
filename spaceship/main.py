import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))+'/../')
from bearlibterminal import terminal as term
from spaceship.setup import setup, setup_font
from spaceship.start import start


if __name__ == "__main__":
    'Keep it as simple as possible'
    setup()
    setup_font('Andale', 8)
    # setup_font('Ibm_cga', 8, 8)
    term.set('window: size=80x50, cellsize=auto, title="Spaceship"')    
    # FH, FW, GH, GW = 16, 16, 24, 40
    # setup_font('Ibm_cga', FW, FH)
    # term.set("window: size={}x{}, cellsize=auto".format(GW, GH))
    start()