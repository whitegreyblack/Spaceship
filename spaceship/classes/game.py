from bearlibterminal import terminal

class Game:
    def __init__(self, font="default"):
        self.__font = font

    def setup(self):
        terminal.open()
        terminal.set("window: size={}x{}, title='{}'".format(
            80, 25, 'Some Game'
        ))
        terminal.refresh()

    def run(self):
        self.setup()
        
        try:
            while True:
                key = terminal.read()
                if key == terminal.TK_ESCAPE or key == terminal.TK_CLOSE:
                    break
        except KeyboardInterrupt:
            pass

        finally:
            terminal.close()

if __name__ == "__main__":
    g = Game()
    g.run()