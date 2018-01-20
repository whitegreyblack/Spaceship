import os
import sys
from bearlibterminal import terminal as term
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)) + '/../')
from .menus.main import Main
from .menus.options import Options
from .menus.game import Start
from .menus.load import Continue
from .menus.make import Create
from .menus.name import Name

class GameEngine:
    def __init__(self):
        # initialize the terminal first or else windows cannot initialize size
        self.setup()

        self.scenes = {
            'main_menu': Main(),
            'options_menu': Options(),
            'start_game': Start(),
            'continue_menu': Continue(),
            'create_menu': Create(),
            'name_menu': Name(),
        }
        
        self.scene = self.scenes['main_menu']

    def setup(self):
        '''sets up instance of terminal'''
        term.open()
        self.setup_font('Ibm_cga', cx=8, cy=8)
        term.set('window: size=80x25, cellsize=auto, title="Spaceship", fullscreen=false')

    def setup_font(self, font, cx=8, cy=None):
        '''Determines font and cell size'''
        if font == "default":
            term.set('font: default, size=8')

        else:
            term.set("window: cellsize=8x8")
            cy = 'x'+str(cy) if cy else ''
            term.set("font: ./spaceship/fonts/{}.ttf, size={}{}".format(
                font, cx, cy))

    def run(self):
        '''Goes through the scenes until exit'''
        self.proceed = True

        while self.proceed:
            ret = self.scene.run()

            if not ret['scene']:
                self.proceed = False

            else:
                try:
                    self.scene = self.scenes[ret['scene']]
                    if ret['kwargs']:
                        self.scene.add_args(**ret['kwargs'])

                except KeyError:
                    self.proceed = False

                else:
                    self.scene.reset()

if __name__ == "__main__":
    e = GameEngine()
    e.run()