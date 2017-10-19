from bearlibterminal import terminal as term
from textwrap import wrap

def center(text, width):
    if isinstance(text, str):
        return width//2-len(text)//2
    if isinstance(text, int):
        return width//2-text//2

def colored(text):
    return "[color=blue]{}[/color]".format(text)

def align(text):
    pass
    
def optionize(text):
    return "[{}] {}".format(text[0], text)

def longest(options):
    return max(map(lambda opt: (len(opt), opt), options))

def join(string, length):
    # use regex to replace [*]
    return "\n\n".join(wrap(string, length))

def split(string, length):
    return wrap(string, length)

def pad(string, center=True, length=0):
    padding = length - len(string)
    if center:
        return padding//2 * " " + string.upper() + (padding+1)//2 * " " if padding else string.upper()
    return string.upper() + padding * " " if padding else string.upper()

def unselected(x, y, text):
    term.puts(x, y, text)

def selected(x, y, text):
    term.bkcolor("white")
    term.puts(x, y, "[color=black]{}[/color]".format(text))
    term.bkcolor("black")

def passed(x, y, text):
    term.bkcolor("grey")
    term.puts(x, y, text)
    term.bkcolor("black")      

def surround(text, char=' ', times=1):
    return char*times+text+char*times

def modify(increment, index, options):
    index += increment
    if not 0 <= index < options:
        index = max(0, min(index, options-1))
    return index

def border(width, heights, character):
    for x in range(width):
        for height in heights:
            term.puts(x, height, character)

def arrow(x, y):
    term.puts(x-2, y, ">")

def point(x, y):
    term.puts(x-2, y, "*")

def barrow(x, y):
    term.puts(x+2, y, "<")

def color(text, color):
    return "[c={}]{}[/c]".format(color, text)

def box(x, y, dx, dy, c):
    for i in range(x, x+dx+1):
        term.puts(i, y, c)
        term.puts(i, y+dy, c)
    for j in range(y, y+dy+1):
        term.puts(x, j, c)
        term.puts(x+dx, j, c)
