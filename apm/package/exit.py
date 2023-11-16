import sys

from .init import import_path

sys.path.append(import_path)

from rich.console import Console
import Tterminal

console = Console()


# def trigger(*argv: dict):
#     if Tterminal.terminal_user == 'root':
#         Tterminal.terminal_user = update_user()
#     console.print('[red]Goodbye![/red]')
#     exit(0)
