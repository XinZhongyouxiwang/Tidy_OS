import sys

from apm.package.init import import_path

sys.path.append(import_path)

command_dict = {'content': {'type': 'C'}}


def trigger(*argv):
    pass
