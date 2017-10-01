from bearlibterminal import terminal as t
from random import randint


def game():
    '''Game body'''
    def setup():
        '''sets up stuff'''
        t.open()
        t.set("window: size=80x25, title: 'Snake'")

    setup()
    score = 0
    maxsize = 80*25
    olddir = None
    x, y = randint(1, 78), randint(1, 23)
    i, j = 40, 12
    while (x, y) == (i, j):
        x, y = randint(1, 78), randint(1, 23)

    while t.has_input():
        t.clear()
        t.puts(0, 24, 'Score: {}'.format(score))
        t.puts(x, y, 'a')
        t.puts(i, j, 'o')
        t.refresh()
        key = t.read()
        if key in (t.TK_CLOSE, t.TK_ESCAPE):
            break
        olddir = key
        if key == t.TK_LEFT:
            i -= 1
        elif key == t.TK_RIGHT:
            i += 1
        elif key == t.TK_UP:
            j -= 1
        elif key == t.TK_DOWN:
            j += 1
        i, j = max(min(i, 79), 0), max(min(j, 23), 0)
        if (i, j) == (x, y):
            score += 1
            x, y = randint(1, 78), randint(1, 23)

game()