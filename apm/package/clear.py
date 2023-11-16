import os

from . import init

command_dict = {
    'key': {'type': 'C'}
}


def clear():
    if init.on_system == 'Windows':
        os.system('cls')
    elif init.on_system == 'Linux':
        os.system('clear')
    else:
        pass


def trigger(*argv):
    clear()
