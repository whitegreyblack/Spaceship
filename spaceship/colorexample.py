from bearlibterminal import terminal as term
from maps import MAP

def colormap(w, h): pass

if __name__ == "__main__":
    term.open()
    cm = colormap(w, h) 
    term.refresh()
    term.read()
    term.close()
