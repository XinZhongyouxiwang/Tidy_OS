from rich.console import Console

console = Console()
import urllib.request

try:
    with console.status('\r正在测试网络连通性...', spinner='line'):
        urllib.request.urlopen('https://www.python.org/')
        console.print('good')
except:
    console.print('网络连通性检测失败.')
