from bearlibterminal import terminal as term

if __name__ == "__main__":
    term.open()
    term.set("window: size=80x25, title='Spaceship'")
    term.printf(1, 1, 'hello')
    term.refresh()

    reader = term.read()
    if reader == term.TK_ESCAPE:
        exit()
    term.close()