import os
import platform
import threading
import time

import keyboard


def clean():
    if platform.system() == 'Windows':
        os.system('cls')
    elif platform.system() == 'Linux':
        os.system('clear')
    else:
        pass


keyboard.add_hotkey('ctrl+l', clean)

while 1:
    print('hello')
    time.sleep(1)
