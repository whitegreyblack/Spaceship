from bearlibterminal import terminal as t
from random import randint


def game():
    '''Game body'''
    def setup():
        '''sets up stuff'''
        t.open()
        t.set("window: size=80x50, cellsize=8x8, title: 'Snake'")
    def end():
        t.clear()
        t.puts(t.state(t.TK_WIDTH)//2-4, t.state(t.TK_HEIGHT)//2-1, 'You Died')
        t.puts(t.state(t.TK_WIDTH)//2-4, t.state(t.TK_HEIGHT)//2+1, 'Score {}'.format(score))
        t.refresh()
        t.read()
        t.close()

    setup()
    score = 0
    maxsize = 80*25
    olddir = t.TK_RIGHT
    x, y = randint(1, t.state(t.TK_WIDTH)-2), randint(1, t.state(t.TK_HEIGHT)-2)
    i, j = 40, 12
    while (x, y) == (i, j):
        x, y = randint(1, t.state(t.TK_WIDTH)-2), randint(1, t.state(t.TK_HEIGHT)-2)

    while True:
        t.clear()
        t.puts(1, 0, 'Score: {}'.format(score))
        t.puts(x, y, 'a')
        t.puts(i, j, 'o')
        t.refresh()
        if t.has_input():
            key = t.read()
        else:
            key = olddir
        if key in (t.TK_CLOSE, t.TK_ESCAPE):
            break
        olddir = key
        if key == t.TK_LEFT:
            i -= 1
            if i < 1:
                end()

        elif key == t.TK_RIGHT:
            i += 1
            if i > t.state(t.TK_WIDTH):
                end()
        elif key == t.TK_UP:
            j -= 1
            if j < 1:
                end()
        elif key == t.TK_DOWN:
            if j > t.state(t.TK_HEIGHT):
                end()
            j += 1
        i, j = max(min(i, t.state(t.TK_WIDTH)-2), 0), max(min(j, t.state(t.TK_HEIGHT)-2), 0)
        if (i, j) == (x, y):
            score += 1
            x, y = randint(1, t.state(t.TK_WIDTH)-2), randint(1, t.state(t.TK_HEIGHT)-2)
        t.delay(100-score)
game()