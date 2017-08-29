from bearlibterminal import terminal as term

if __name__ == "__main__":
    term.open()
    term.puts(0,0,'[color={}]a[/color]'.format("#ff0000ff"))
    term.refresh()
    term.read()
    term.close()
