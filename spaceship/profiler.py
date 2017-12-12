import cProfile
import io
import pstats
from .start import start
from .setup_game import setup_font
from bearlibterminal import terminal as term

if __name__ == "__main__":
    pr = cProfile.Profile()
    pr.enable()
    # =========================
    term.open()
    setup_font('Ibm_cga', 8, 8)
    term.set('window: size=80x25, cellsize=auto, title="Spaceship", fullscreen=false') 
    start()
    # =========================
    pr.disable()
    s = io.StringIO()
    sortby = 'cumulative'
    ps = pstats.Stats(pr, stream=s).sort_stats(sortby)
    ps.print_stats()
    print(s.getvalue())