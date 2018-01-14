import os
import sys
import shelve
import random
from collections import namedtuple
from bearlibterminal import terminal as term
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)) + '/../')
'''
Notes: Scene Connections
    def connect_scenes(scene_a, scene_b):
        scene_a.add_scene(scene_b)
        scene_b.add_scene(scene_a)

        scene_a.add_child_scene(scene_b)
        scene_b.add_parent_scene(scene_a)
'''
class Scene:
    def __init__(self, scene_id):
        '''Initializes window and screen dimensions and title for the scene'''
        # self.width, self.height = width, height
        self.reset_size()
        self.sid = scene_id

        self.proceed = True

        # scenes is a dictionary holding other scene objects
        self.scenes = {}
        self.ret = {
            'scene': '',
            'kwargs': None,
        }
        self.setup()

    def __repr__(self):
        return self.sid

    def add_args(self, **kwargs):
        if self.ret['kwargs'] is None:
            self.ret['kwargs'] = {k: v for k, v in kwargs.items()}
        else:
            self.ret['kwargs'].update({k: v for k, v in kwargs.items()})

    def reset_size(self):
        self.width = term.state(term.TK_WIDTH)
        self.height = term.state(term.TK_HEIGHT)

    def setup(self):
        pass
    
    def run(self):
        while self.proceed:
            self.draw()
        
        self.proceed = True
        return self.ret

    def draw(self):
        pass

    def reset(self):
        pass

    @property
    def height(self):
        return self.__height

    @height.setter
    def height(self, h):
        self.__height = h

    @property
    def width(self):
        return self.__width

    @width.setter
    def width(self, w):
        self.__width = w

    def check_scene(self, scene):
        # if scene.title in self.scenes.keys():
        #     raise ValueError('Same title already in scene')
        # elif scene.width != self.width:
        m = None
        if self == scene:
            m = 'Incoming scene is duplicate of current scene'

        elif scene.width != self.width:
            m = 'Incoming scene does not have the same width as current scene: '
            m += 'CUR: {}x{} != INC: {}x{}'.format(
                self.width, 
                self.height,
                scene.width,
                scene.height)

        elif scene.height != self.height:
            m = 'Incoming scene does not have the same height as current scene:'
            m += ' CUR: {}x{} != INC: {}x{}'.format(
                self.width, 
                self.height,
                scene.width,
                scene.height)
        else:
            for key in self.scenes.keys():
                if scene.sid in self.scenes[key].keys():
                    m = 'Same Title already in scene'
        if m:
            raise ValueError(m)
        return True

    def scene(self, s_id):
        for _, scenes in self.scenes.items():
            for sid, scene in scenes.items():
                if sid == s_id:
                    return scene

    def scene_child(self, sid):
        if isinstance(sid, Scene):
            sid = sid.sid

        try:
            scene = self.scenes[1][sid]

        except KeyError:
            raise KeyError('No parent scene with that title')

        except:
            raise

        else:
            return scene

    @property
    def children(self):
        '''Returns a list of children scene objects'''
        # return [self.scenes[(title, scene for title, scene in self.scenes.keys() if scene == 0]
        if 1 not in self.scenes.keys():
            return []

        elif len(self.scenes[1].keys()) == 1:
            return list(self.scenes[1].values())

        # return [self.scenes[1][title] for title in self.scenes[1].keys()]
        return [scene for _, scene in self.scenes[1].items()]


    def add_scene_child(self, scene):
        self.check_scene(scene)
        # self.scenes[(scene.title, 0)] = scene
        # self.scenes[0][scene.title] = scene
        if 1 not in self.scenes.keys():
            self.scenes[1] = { scene.sid: scene }

        else:
            self.scenes[1][scene.sid] = scene
    
    def scene_parent(self, sid):
        if isinstance(sid, Scene):
            sid = sid.sid

        try:
            scene = self.scenes[0][sid]

        except KeyError:
            raise KeyError('No parent scene with that title')

        except:
            raise
        
        else:
            return scene

    def add_scene_parent(self, scene):
        self.check_scene(scene)
        # self.scenes[(scene.title, 1)] = scene
        # self.scenes[1][scene.title] = scene
        if 0 not in self.scenes.keys():
            self.scenes[0] = { scene.sid: scene }
 
        else:
            self.scenes[0][scene.sid] = scene 

    @property
    def parents(self):
        '''Returns a list of parent scene objects'''
        # return [self.scenes[(title, scene)] for title, scene in self.scenes.keys() if scene == 1]
        if 0 not in self.scenes.keys():
            return []

        elif len(self.scenes[0].keys()) == 1:
            return list(self.scenes[0].values())
        
        # return [self.scenes[0][sid] for sid in self.scenes[0].keys()]
        return [scene for _, scene in self.scenes[0].items()]