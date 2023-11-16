import os
import sys

from .init import import_path, index_path, on_system

sys.path.append(import_path)

import terminal
from rich.console import Console
from rich.markdown import Markdown

console = Console()
command_dict = {
    'package_name': {'type': 'E'}
}

help = """
help [command]
    command - 需要显示的帮助的命令的名称, 可使用apm packagelist 命令查看
"""


def trigger(*argv: dict):
    argvs = argv[0]
    if len(argvs['dl']['package_name']) == 0 or argvs['dl']['package_name'] == 'help':
        console.print(help)
        print(argvs)
    else:

        if terminal.file_driver.exist(f"{index_path}/package/{argvs['dl']['package_name']}.py"):
            try:
                sys.path.append(import_path)
                exec(f"from apm.package.{argvs['dl']['package_name']} import help as {argvs['dl']['package_name']}_help")
                console.print(eval(argvs['dl']['package_name'] + '_help'))
                terminal.file_driver.remove('{}/temp/help_{}'.format(index_path, argvs['dl']['package_name']))
            except ImportError as e:
                console.print(e, 'ImportError', style='red')
            except Exception as e:
                console.print(e, '未知错误', style='red')
        else:
            # console.print('无法找到此命令的help', style='red')
            console.print(argvs)