import sys
import os

import terminal

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from terminal import file_driver


class UserExistError(ValueError):
    def __str__(self):
        pass


class USER_SETTING:
    def __init__(self, config_file: str):
        self.config_file_path = config_file
        try:
            self.config_file: dict = file_driver.read(self.config_file_path, 'json')
        except FileNotFoundError:
            raise FileNotFoundError(
                'user.py: user config file can not find.Please check that the file location is correct!')

    def change_configfile(self):
        source: dict = file_driver.read(self.config_file_path, 'json')
        if not self.config_file == source:
            a = set(self.config_file.items()) ^ set(source.items())

    def add_user(self, username: str, password: str):
        if username not in self.config_file:
            self.config_file[username] = password
            self.change_configfile()
        else:
            raise UserExistError(f'{username} is exist in the {self.config_file_path}')


if __name__ == '__main__':
    user = USER_SETTING('./user.json')
    user.add_user('admin', 'chd')
