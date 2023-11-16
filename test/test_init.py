import platform
import os
import rich
from rich.console import Console
console = Console()

on_system = platform.system()

if on_system == 'Windows':
    index_path = os.path.normpath('/'.join(os.path.dirname(__file__).split('\\')[0:-1]))
    index_path_list = index_path.split('\\')
    index_path_list = index_path_list[0:index_path_list.index('Tterminal')+1]
    import_path = '\\'.join(index_path_list)
elif on_system == 'Linux':
    index_path = os.path.normpath('/'.join(os.path.dirname(__file__).split('/')[0:-1]))
    index_path_list = index_path.split('/')
    index_path_list = index_path_list[0:index_path_list.index('Tterminal')+1]
    import_path = '/'.join(index_path_list)
else:
    index_path = None

if __name__ != '__main__':
    console.print('[red]You are using the production environment.[/red]')


if __name__ == '__main__':
    print()
    console.print('[red]You are using the production environment.[/red]')
    import sys
    sys.path.append(import_path)
    print(f'IndexPath: {index_path}')
    print(f'ImportPath: {import_path}')
    print(f'OnSystem: {on_system}')
