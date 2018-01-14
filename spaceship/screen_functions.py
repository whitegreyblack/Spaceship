from bearlibterminal import terminal as term
from textwrap import wrap

def center(text, width):
    '''Returns x position for string given a width length'''
    if isinstance(text, str):
        text = len(text)

    return width // 2 - text // 2

def colorize(text, color):
    '''Returns a BLT colored encapsulated text'''
    return "[c={}]{}[/c]".format(color, text)

def optionize(text):
    '''return text as an option string surrounded by brackets'''
    return "[{}] {}".format(text[0], text)

def longest(options):
    '''Lambda function to return longest string in the options array'''
    return max(map(lambda opt: (len(opt), opt), options))

def join(string, length, delim="\n"):
    '''Joins string using wrap to split string into array, then adds
    delimiter if specified ontop of a newline delimiter'''
    # use regex to replace [*]
    return ("{}\n".format(delim)).join(wrap(string, length))

def split(string, length):
    '''splits text using length and wrap function from textwrap library'''
    return wrap(string, length)

def pad(string, center=True, length=0):
    '''Adds equal spacing to the sides of a string unless center is false,
    which pads the leftside instead
    '''
    padding = length - len(string)
    if padding <= 0:
        return string.upper()

    if center:
        l_pad = " " * (padding // 2)
        r_pad = " " * ((padding + 1) // 2)
        
        return l_pad + string.upper() + r_pad

    return string.upper() + " " * padding

def surround(text, char=' ', times=1, length=0):
    '''Surrounds the text inputted with a character by a number of times
    or until given length is reached'''
    if length:
        while len(text) <= length:
            if len(text) % 2:
                text = text + char
                
            else:
                text = char + text

        return text

    else:
        pad = char * times
        
        return pad + text + pad

def switch(x, y, text, bg_before='black', bg_after='black', color='white'):
    '''Abstract function in place of UNSELECTED, SELECTED, and PASSED'''
    if bg_before == bg_after:
        term.puts(x, y, colorize(text, color))

    else:
        term.bkcolor(bg_before)
        term.puts(x, y, colorize(text, color))
        term.bkcolor(bg_after)

def modify(increment, index, options):
    '''Increments an integer parameter index and clamps the value between
    0 and length of options.
    '''
    index += increment
    if not 0 <= index < options:
        index = max(0, min(index, options-1))
    return index

def border_vertical(x, heights, width, character):
    '''Using a single character, fills the screen starting at row heights
    and for col width

    call ex. :- border(w, [h, h], '#')
    '''
    for height in heights:
        switch(x, height, character * width)

def border_vertical(y, widths, height, character):
    for width in widths:
        for h in height:
            switch(x, height, character)

def arrow(x, y, color="black"):
    '''Adds a greater than sign at the target location on the terminal'''
    switch(x, y, '>')

def point(x, y, color="black"):
    '''Adds a star sign at the location on the terminal'''
    switch(x, y, '*')

def barrow(x, y, color="black"):
    '''Adds a less than sign at the target location on the terminal'''
    switch(x, y, '<')

def box(x, y, dx, dy, c):
    '''Prints a box on the terminal with the given coordinates and character'''
    for i in range(x, x + dx + 1):
        term.puts(i, y, c)
        term.puts(i, y + dy, c)

    for j in range(y, y + dy + 1):
        term.puts(x, j, c)
        term.puts(x + dx, j, c)

def toChr(intval):
    try:
        return chr(toInt(intval))
    except TypeError:
        print("TOCHR ERROR: ", intval)
        raise

def toInt(hexval):
    try:
        return int(hexval, 16)
    except TypeError:
        print("TOINT ERROR: ", hexval)
        raise

def alphabetize(text):    
    return list(map(lambda x: toChr(alphabet[x]) if x in alphabet.keys() else x, list(text)))