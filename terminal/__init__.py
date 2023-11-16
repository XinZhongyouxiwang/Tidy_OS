import os
import platform
import datetime
import sys
from typing import Literal
from rich.console import Console

console = Console()
import keyboard

on_system = platform.system()

work_directory = os.getcwd()

work_file = __file__

if on_system == 'Windows':
    index_path = os.path.normpath('/'.join(os.path.dirname(__file__).split('\\')[0:-1]))
    index_path_list = index_path.split('\\')
    index_path_list = index_path_list[0:index_path_list.index('Tterminal') + 1]
    import_path = '\\'.join(index_path_list)
elif on_system == 'Linux':
    index_path = os.path.normpath('/'.join(os.path.dirname(__file__).split('/')[0:-1]))
    index_path_list = index_path.split('/')
    index_path_list = index_path_list[0:index_path_list.index('Tterminal') + 1]
    import_path = '/'.join(index_path_list)
else:
    index_path = None

sys.path.append(os.path.normpath(import_path))

from terminal import file_driver


def write_log(file_name: str, log_content):
    log_name = f'{index_path}/log/{datetime.datetime.now():%Y%m%d%H%M%S}_{file_name}.log'
    file_driver.makefile(log_name)
    file_driver.write(log_name, log_content)


def add_temp(filename, content=''):
    if type(content) != str:
        file_driver.makefile(f'{index_path}/temp/{filename}')
        file_driver.write(f'{index_path}/temp/{filename}', content, )


def print_log(log_content, log_type: Literal['w', 'e']):
    if log_type == 'w':
        console.print('Warning: ', log_content, style='yellow')
    elif log_type == 'e':
        console.print('Error', log_content, style='red')
    else:
        raise TypeError("log_type must be 'w' or 'e'")


__all__ = ['on_system', 'work_directory', 'work_file', 'index_path', 'file_driver', 'user', 'import_path',
           'write_log',
           'parsing', ]

if __name__ == '__main__':
    pass
