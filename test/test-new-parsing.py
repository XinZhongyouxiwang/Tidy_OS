# import os
# import sys
#
# sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
#
# from terminal import index_path
# from terminal import import_path
# from terminal import file_driver
#
# from terminal import file_driver
# sys.path.append(import_path)
#
# l_all_command = []
# d_all_command = file_driver.read(f'{index_path}/apm/_command.json', 'json')
#
#
# def get_argv(file:str, command:str = ''):
#     d_command = file_driver.read(f'{import_path}/apm/_command.json', 'json')
#     file = file[:-3]
#     try:
#         exec(f'from apm.package import {file}')
#     except Exception:
#         return 400
#
#     if ' ' in command:
#         l
