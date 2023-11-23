# coding=utf-8

"""
test
"""
import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from bin import index_path
from bin import import_path
from bin import file_driver
from bin.user import USER_SETTING


sys.path.append(import_path)


class Terminal:
    def __init__(self, name, user: str = '', path: str = ''):
        self.name = name
        if user != '':
            USER_SETTING.
            self.user = user
        else:
        self.path = path
