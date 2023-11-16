import os
import time

import keyboard
from rich.console import Console
import datetime

console = Console()

while True:
    status = os.system("ping 192.168.31.1 -n 1")
    if status != 0:
        status_in = os.system("ping baidu.com -n 1")
        if status_in != 0:
            console.clear()
            console.print(f"[bold red]{datetime.datetime.now()}: 网络连接失败 路由器已离线!", justify='center')
            console.print('[确定]', style='#FF9933', justify='center')
            keyboard.wait('enter', True)
        else:
            console.clear()
            console.print(f"[bold red]{datetime.datetime.now()}: 网络连接失败 无法连接外网!", justify='center')
            console.print('[确定]', style='#FF9933', justify='center')
            keyboard.wait('enter', True)
    time.sleep(1)
