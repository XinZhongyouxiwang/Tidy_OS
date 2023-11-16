import sys
from apm.package.init import import_path

command_dict = {
    'fileA': {'type': 'E'},
    'operation': {'type': 'E'},
    'fileB': {'type': 'E'}
}

help = """
# cat
"""

sys.path.append(import_path)
g_argv = {}


def main():
    print(g_argv)


def trigger(argv=None):
    global g_argv
    if argv is None:
        argv = {}
    else:
        g_argv = argv
    if 'operation' in argv['dl']:
        pass
    else:
        try:
            # print(file_driver.read(f'{Tterminal.physical_directory}/{argv["dl"]["fileA"]}'))
            print(argv['dl']['fileA'])
        except FileNotFoundError:
            print(f'[red]file "{argv["dl"]["fileA"]}" not found.[/red]')
