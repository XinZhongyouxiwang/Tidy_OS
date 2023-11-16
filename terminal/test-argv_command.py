"""
input -> ls -l
parsing -> ls , -l
send -> find: _command.json

"""
from typing import List

command_dict = {
    "-l": {
        "long": [
            "--list"
        ],
        "type": 'A'
    },
    "-a": {
        "long": [
            "--all"
        ],
        "type": "B"
    }
}

import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from terminal import index_path
from terminal import import_path
from terminal import file_driver

sys.path.append(import_path)

_command_dict = {}


def trigger(file):
    global _command_dict
    global command
    if file_driver.file_exist(f'{index_path}/apm/package/{file}.py'):
        try:
            exec(f'from apm.package import {file}')
            _command_dict = command

        except ImportError as e:
            raise ImportError(f'导入错误, 报错信息:\n{e}')

        try:
            exec(f'{file}.trigger()')
        except Exception as e:
            raise RuntimeError(f'argv_parsing.trigger: 函数运行时发生错误, 报错信息:\n{e}')
    else:
        raise FileNotFoundError('argv_parsing.trigger: 需要导入的文件不存在')


command = 'ls -l'
# find ls command

if ' ' in command:
    command_list = command.split(' ')
    # find -> command_list[0]
    # argv_list = command_dict[1:]
    # read command_dict
    # find argv -> '-l' -> ['type']
    # type : A\B\C\D\E\F\G\H\I\J\K\L\M\N\O\P\Q\R\S\T\U\V\W\X\Y\Z
    # 

else:
    # find command
    ...

trigger('cat')

return_dict = {}

print('\ncommand: ', command, '\n')

for i in command_dict:

    if command_dict[i]['type'] == 'A':
        if i in command_list:
            return_dict[i] = True
        else:
            return_dict[i] = False
            if 'long' in command_dict[i]:
                for c_long in command_dict[i]:
                    if c_long in command_list:
                        return_dict[i] = True
                        break
                    else:
                        return_dict[i] = False

    elif command_dict[i]['type'] == 'B':
        if i in command_list:
            try:
                return_dict[i] = command_list[command_list.index(i)+1]
            except IndexError as e:
                raise IndexError(f'序列超出, 报错信息:\n{e}')
        else:
            return_dict[i] = ''
            for c_long in command_dict[i]['long']:
                if c_long in command_list:
                    try:
                        return_dict[i] = command_list[command_list.index(c_long)+1]
                    except IndexError as e:
                        raise IndexError(f'序列超出, 报错信息: \n {e}')
                    break
    else:
        raise RuntimeError('传参错误')



print(return_dict)
