# coding=utf-8

"""
This file is part of the parameter parsing file in the Tterminal terminal, do not delete!
filename: parsing.py
creation time: 20230724 16:42
version:20230724-0.01
"""
import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from terminal import index_path
from terminal import import_path
from terminal import file_driver

sys.path.append(import_path)

_command_dict = {}
l_all_command = []
d_all_command = file_driver.read(f'{index_path}/apm/_command.json', 'json')


def get_argv(file, command: str):
    global _command_dict
    file = file[:-3]
    try:
        exec(f'from apm.package import {file}')
    except Exception:
        return 400

    if ' ' in command:
        l_argv = command.split(' ')[1:]
    else:
        l_argv = []

    try:
        return_dict = {}
        _command_dict = eval(f'{file}.command_dict')

    except Exception:
        return 401

    return_dict = {'dl': {}}
    for i, n in zip(_command_dict, range(len(l_argv))):
        if _command_dict[i]['type'] == 'A':
            if i in l_argv:
                return_dict[i] = True
            else:
                return_dict[i] = False
                if 'long' in _command_dict[i]:
                    for c_long in _command_dict[i]['long']:
                        if c_long in l_argv:
                            return_dict[i] = True
                            break
                        else:
                            return_dict[i] = False

        elif _command_dict[i]['type'] == 'B':
            if i in l_argv:
                if \
                        file_driver.read(f'{index_path}/config/setting.json', 'json')['i_terminal'][
                            'simplify-error-messages'][
                            1]:
                    try:
                        return_dict[i] = l_argv[l_argv.index(i) + 1]
                    except IndexError as e:
                        raise IndexError(f'序列超出, 报错信息:\n{e}')
                else:
                    return_dict[i] = l_argv[l_argv.index(i) + 1]
            else:
                return_dict[i] = None
                for c_long in _command_dict[i]['long']:
                    if c_long in l_argv:
                        if file_driver.read(f'{index_path}/config/setting.json', 'json')['i_terminal'][
                            'simplify-error-messages'][1]:
                            try:
                                return_dict[i] = l_argv[l_argv.index(c_long) + 1]
                            except IndexError as e:
                                raise IndexError(f'序列超出, 报错信息: \n {e}')
                        else:
                            return_dict[i] = l_argv[l_argv.index(c_long) + 1]

                        break
        elif _command_dict[i]['type'] == 'C':  # return : list
            return_dict['return_list'] = l_argv
        elif _command_dict[i]['type'] == 'D':
            for e_argv in l_argv:
                if '=' in e_argv:
                    try:
                        key = e_argv[0:e_argv.find('=')]
                        value = e_argv[e_argv.find('=') + 1:]
                    except Exception as e:
                        raise RuntimeError(e)

                    if key in _command_dict:
                        return_dict[key] = value

                    if 'long' in _command_dict[i]:
                        if key in _command_dict[i]['long']:
                            try:
                                key = e_argv[0:e_argv.find('=')]
                                value = e_argv[e_argv.find('=') + 1:]
                            except Exception as e:
                                raise RuntimeError(e)
                            if key in _command_dict:
                                return_dict[key] = value
        elif _command_dict[i]['type'] == 'MAB':
            for mab_c in l_argv:
                if '-' in mab_c:
                    if mab_c not in _command_dict:
                        if mab_c.find('-') == 0:
                            for mab_ in mab_c[1:]:
                                if f'-{mab_}' in _command_dict:
                                    return_dict[f'-{mab_}'] = True
        elif _command_dict[i]['type'] == 'E':
            return_dict['dl'][i] = l_argv[n]
        else:
            raise RuntimeError('parsing.py: 传参错误')

    return return_dict


def trigger(key: str, command: str):
    if key in d_all_command:
        filename = d_all_command[key]['file']
    else:
        return 400
    if file_driver.file_exist(f'{index_path}/apm/package/{filename}'):

        try:
            if file_driver.read(f'{index_path}/config/setting.json', 'json')['i_terminal']['simplify-error-messages'][
                1]:

                exec(f'from apm.package import {d_all_command[key]["file"][:-3]}')
            else:
                exec(f'from apm.package import {d_all_command[key]["file"][:-3]}')
        except ImportError:
            raise ImportError('导入错误')
        if file_driver.read(f'{index_path}/config/setting.json', 'json')['i_terminal']['simplify-error-messages'][
            1]:
            try:
                exec(f'{filename[:-3]}.trigger({get_argv(filename, command)})')
            except:
                raise RuntimeError('函数运行时错误')
        else:
            exec(f'{filename[:-3]}.trigger({get_argv(filename, command)})')

    else:
        raise FileNotFoundError('指定的python文件不存在')


def i_terminal(command: str = ''):
    if command == '':
        return 200
    global l_all_command
    if ' ' in command:
        head = command.split(' ')[0]
    else:
        head = command

    l_all_command = []
    t = ''
    for t in d_all_command:
        if 'trigger' in d_all_command[t]:
            l_all_command.extend(d_all_command[t]['trigger'])
            if head in l_all_command:
                break
        else:
            return 404
    # print(l_all_command)

    if head in l_all_command:
        if file_driver.read(f'{index_path}/config/setting.json', 'json')['i_terminal']['simplify-error-messages'][0]:
            try:
                trigger(t, command)
                return 200
            except ImportError:
                return 401
            except RuntimeError:
                return 402
            except FileNotFoundError:
                return 403
            except Exception:
                return 405
        else:
            trigger(t, command)
    else:
        if file_driver.read(f'{index_path}/config/setting.json', 'json')['i_terminal']['simplify-error-messages'][1]:
            return 400
        else:
            raise FileNotFoundError('没有这个文件')


if __name__ == '__main__':
    i_terminal('help ')