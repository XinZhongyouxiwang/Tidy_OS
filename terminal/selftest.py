# 导入相关模块 Import related modules
import sys
import os
import platform

on_system = platform.system()

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

sys.path.append(import_path)

from terminal import file_driver


def startup_self_test():
    try:
        # test _command.json file
        file_driver.read('../apm/_command.json', 'json')
        #
    except Exception as e:
        raise e
