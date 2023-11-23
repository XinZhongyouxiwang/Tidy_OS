import os
import sys
import keyboard
from rich.console import Console

# 对整体terminal添加import 路径
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import bin
from bin import file_driver

console = Console()


class Terminal:
    def __init__(self, path: str = None, app_path: str = None, run: tuple = False):
        if path is None:
            self.work_directory = os.getcwd()
        else:
            if file_driver.isfile(path):
                self.work_directory = path
            else:

        if app_path is not None:
            self.app_path = os.path.join(self.work_directory, self.app_path)
        if file_driver.exist(self.app_path):
            self.app_icon = None
            self.terminal_name = 'Tterminal'
