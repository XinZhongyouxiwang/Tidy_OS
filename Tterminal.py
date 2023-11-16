import os
import sys
import keyboard
from rich import print

# 对整体terminal添加import 路径
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import terminal
from terminal import parsing
from terminal import file_driver
from terminal import index_path

terminal_user = 'root'
terminal_path = '/'
terminal_name = 'DESKTOP'
current_program = 'bash'
setting = file_driver.read(f'{index_path}/config/setting.json', 'json')
debug = True

def clean():
    keyboard.press_and_release('home')
    keyboard.write('clear ')
    keyboard.press_and_release("enter")


keyboard.add_hotkey('ctrl+l', clean)


def init():
    if debug:
        setting_config = file_driver.read(f'{index_path}/config/setting.json', 'json')
        setting_config['i_terminal']['simplify-error-messages'] = [False, False]
        file_driver.write(f'{index_path}/config/setting.json', setting_config, 'json')
    else:
        setting_config = file_driver.read(f'{index_path}/config/setting.json', 'json')
        setting_config['i_terminal']['simplify-error-messages'] = [True, True]
        file_driver.write(f'{index_path}/config/setting.json', setting_config, 'json')


if __name__ == '__main__':
    init()
    if len(sys.argv) > 2:
        if '--debug' in sys.argv[1:]:
            if '--exit' in sys.argv[1:]:
                print(parsing.i_terminal(''.join(sys.argv[1:])))
                exit(0)
            else:
                print(parsing.i_terminal(''.join(sys.argv[1:])))
        else:
            if '--exit' in sys.argv[1:]:
                parsing.i_terminal(''.join(sys.argv[1:]))
                exit(0)
            else:
                parsing.i_terminal(''.join(sys.argv[1:]))


    # physical_directory 赋值
    if setting['terminal']['root-default-path'] == '/':
        setting['terminal']['root-default-path'] = terminal.work_directory
        file_driver.write(f'{index_path}/config/setting.json', setting, 'json')
    print(os.getcwd())
    while True:
        if terminal_user == 'root':
            print(f'\r{terminal_user}@{terminal_name}:{terminal_path}[green]#[/green] ', end='')
            command = str(input())
            if debug:
                print(parsing.i_terminal(command))
            else:
                parsing.i_terminal(command)

        else:
            print(f'\r{terminal_user}@{terminal_name}:{terminal_path}[green]$[/green] ', end='')
            command = str(input())
            print(parsing.i_terminal(command))