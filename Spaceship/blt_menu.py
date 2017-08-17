from bearlibterminal import terminal

terminal.open()
terminal.printf(1, 1, 'hello')
terminal.refresh()

reader = terminal.read()
if reader == terminal.TK_ESCAPE:
    exit()
terminal.close()
