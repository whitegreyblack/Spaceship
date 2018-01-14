import win32api
import time
from threading import Thread


class Recorder:
    def __init__(self):
        self.special_keys = [0x01, 0x02, 0x10, 0x20]

        self.special = {0x01: 'leftClick',
                        0x02: 'rightClick',
                        0x10: 'shift',
                        0x20: 'space'}
        self.times = []
        self.pressed = []

    def record(self):
        Thread(target=self.key_down_time, args=(0x57,)).start()
        Thread(target=self.key_down_time, args=(0x41,)).start()
        Thread(target=self.key_down_time, args=(0x53,)).start()
        Thread(target=self.key_down_time, args=(0x44,)).start()

    def key_down_time(self, key):
        while True:
            if win32api.GetAsyncKeyState(key):
                print(chr(key), 'was pressed')
            time.sleep(0.05)

r = Recorder()

r.record()
