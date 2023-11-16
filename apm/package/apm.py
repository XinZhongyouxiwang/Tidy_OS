from rich.console import Console
import sys
from .init import import_path

sys.path.append(import_path)

console = Console()
command_dict = {
    'command': {'type': 'E'},
    'operation': {'type': 'E'}
}

help = """
apm 是一个在Tidy terminal 上方便管理插件包的工具
参数:
    install <package name> -- 安装某个tapm软件包
    uninstall <package name> -- 卸载某个tapm软件包
    update -- 获取更新列表
    list -- 查看软件包列表
    search <package name> -- 在github.com上搜索tamp软件包
    help -- 输出本页面

"""


def install(command):
    print('install')


def uninstall(command):
    pass


def update(command):
    pass


def list():
    pass


def search(command):
    pass
def __help__(command):
    pass

def unknown(*argv):
    argv = argv[0]
    console.print('E: apm.py: 未知参数', style='red')


def trigger(*argv):
    argv = argv[0]
    print(argv)
