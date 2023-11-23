import hashlib
import ssl
import urllib.request
from concurrent.futures import ThreadPoolExecutor
from functools import partial
from threading import Event
from typing import Iterable
from urllib.request import urlopen
from git.repo import Repo
import socket
import subprocess
import webbrowser
import keyboard
import psutil
import json
import os
import pathlib
import shutil
import signal
import getpass
import string
from rich.console import Console
from rich.progress import (
    BarColumn,
    DownloadColumn,
    Progress,
    TaskID,
    TextColumn,
    TimeRemainingColumn,
    TransferSpeedColumn,
)

progress = Progress(
    TextColumn("[bold blue]{task.fields[filename]}", justify="right"),
    BarColumn(bar_width=None),
    "[progress.percentage]{task.percentage:>3.1f}%",
    "•",
    DownloadColumn(),
    "•",
    TransferSpeedColumn(),
    "•",
    TimeRemainingColumn(),
)

done_event = Event()
console = Console()
a = 0
n_select = 0
s_i = 0

disk = str(psutil.disk_partitions())
disk_device = r'device'

import json
import os
import shutil
from typing import Literal


def exist(path: str | list[str]) -> bool | list[bool]:
    """
    检查文件是否存在
    :param path: 文件路径 Type: str list[str]
    """
    if type(path) is str:
        if os.path.exists(path):
            return True
        else:
            return False
    elif type(path) is list:
        return_list = []
        for i in path:
            if os.path.exists(i):
                return_list.append(True)
            else:
                return_list.append(False)

        return return_list
    else:
        raise TypeError("path must be str or list")


def isfile(path: str | list[str]) -> bool | list[bool]:
    """
    判断路径是文件夹还是文件
    :param path: 路径 Type: str | list[str]
    :return: bool | list[bool]
    """
    return_list = []
    if type(path) is str:
        if exist(path):
            if os.path.isfile(path):
                return True
            else:
                return False
        else:
            raise FileNotFoundError(f'file_driver: can not found the "{path}"')
    elif type(path) is list:

        for i in path:
            if exist(i):
                if os.path.isfile(i):
                    return_list.append(True)
                else:
                    return_list.append(False)
            else:
                raise FileNotFoundError(f'file_driver: can not found the "{i}"')

        return return_list
    else:
        raise TypeError("path must be str or list")


def mkdir(*path: str) -> None:
    """
    创建文件夹
    :param path: 路径 Type: str
    :return: None
    """
    for i in path:
        if not exist(i):
            os.mkdir(i)
        else:
            raise FileExistsError(f'file_driver: the "{i}" is exist')


def makefile(*path: str) -> None:
    """
    创建文件
    :param path: 路径 Type: str
    :return: None
    """
    for i in path:
        if not exist(i):
            file = open(i, 'x')
            file.write('')
            file.close()
        else:
            raise FileExistsError(f'file_driver: the "{i}" is exist')


def read(path: str, mode: Literal['r', 'rb', 'json']) -> str | dict | bytes:
    if mode == 'r':
        if isfile(path):
            file = open(path, 'r')
            file_read: str = file.read()
            file.close()
            return file_read
        else:
            raise IsADirectoryError('file_driver: the path is a directory')
    elif mode == 'rb':
        if isfile(path):
            file = open(path, 'rb')
            file_read: bytes = file.read()
            file.close()
            return file_read
        else:
            raise IsADirectoryError('file_driver: the path is a directory')
    elif mode == 'json':
        if isfile(path):
            file = open(path, 'r')
            content: dict = json.loads(file.read())
            file.close()
            return content
        else:
            raise IsADirectoryError('file_driver: the path is a directory')


def write(path: str, content: str | dict | bytes, mode: Literal['w', 'a', 'json']) -> None:
    if mode == 'w':
        if isfile(path):
            file = open(path, 'w')
            if type(content) is str:
                file.write(content)
                file.close()
            else:
                raise
        else:
            raise IsADirectoryError('file_driver: the path is a directory')
    elif mode == 'a':
        if isfile(path):
            file = open(path, 'a')
            file.write(content)
            file.close()
        else:
            raise IsADirectoryError('file_driver: the path is a directory')
    elif mode == 'json':
        if isfile(path):
            if type(content) is dict:
                file = open(path, 'w')
                file.write(json.dumps(content))
                file.close()
            else:
                raise TypeError('file_driver: the content is not a dict')
        else:
            raise IsADirectoryError('file_driver: the path is a directory')
    else:
        raise TypeError('file_driver: the mode is not valid')


def remove(path: str, mode: Literal['f', 'd']) -> None:
    if mode == 'f':
        if isfile(path):
            os.remove(path)
        else:
            raise IsADirectoryError('file_driver: the path is a directory')
    elif mode == 'd':
        if exist(path):
            shutil.rmtree(path)
        else:
            raise FileNotFoundError('file_driver: the path does not exist')


def handle_sigint(signum, frame):
    done_event.set()


signal.signal(signal.SIGINT, handle_sigint)


def copy_url(task_id: TaskID, url: str, path: str) -> None:
    progress.console.log(f"Requesting {url}")
    response = urlopen(url)
    progress.update(task_id, total=int(response.info()["Content-length"]))
    with open(path, "wb") as dest_file:
        progress.start_task(task_id)
        for data in iter(partial(response.read, 32768), b""):
            dest_file.write(data)
            progress.update(task_id, advance=len(data))
            if done_event.is_set():
                return
    progress.console.log(f"Downloaded {path}")


def download(urls: Iterable[str], dest_dir: str):
    with progress:
        with ThreadPoolExecutor(max_workers=4) as pool:
            for url in urls:
                filename = url.split("/")[-1]
                dest_path = os.path.join(dest_dir, filename)
                task_id = progress.add_task("download", filename=filename, start=False)
                pool.submit(copy_url, task_id, url, dest_path)


def sha256sum(path):
    if not os.path.isfile(path):
        print(f'{path} is not a file')
        exit(1)
    with open(path, "rb") as f:
        sha256 = hashlib.sha256(f.read()).hexdigest()
    return sha256


class Select:
    def __init__(self, title: str, options: list):
        self.title = title
        self.options = options
        self.n_select = 0
        self.a = 1

    def up(self):
        if self.n_select > 0:
            self.n_select -= 1
        self.display()

    def down(self):
        if self.n_select < len(self.options) - 1:
            self.n_select += 1
        self.display()

    def display(self):
        console.clear()
        console.print(self.title + '(使用上下键选择)', justify='center')
        for l, c in enumerate(self.options):
            if l == self.n_select:
                console.print(f'{l + 1}. {c}', justify='center', style='#FF9933')
            else:
                console.print(f'{l + 1}. {c}', justify='center')

    def select(self) -> int:
        self.display()
        keyboard.add_hotkey('up', self.up)
        keyboard.add_hotkey('down', self.down)
        keyboard.wait('enter', True)
        console.clear()
        return self.n_select

    def number(self) -> int:
        return self.select() + 1

    def content(self) -> str:
        return self.options[self.select()]


class YN(Select):
    def __init__(self, title: str):
        super().__init__(title, ['是', '否'])

    def display(self):
        console.clear()
        console.print(self.title + '(确认以继续)', justify='center')
        for l, c in enumerate(self.options):
            if l == self.n_select:
                console.print(f'{l + 1}. {c}', justify='center', style='#FF9933')
            else:
                console.print(f'{l + 1}. {c}', justify='center')


class Verify(Select):
    def __init__(self, title: str):
        super().__init__(title, ['确认'])


if __name__ == '__main__':
    start_install = Select('开始Tidy terminal 的安装\n(您可以选择是否继续安装)', ['继续', '退出'])
    if start_install.number() == 2:
        console.print('您已结束Tidy terminal 的安装, Bye!\n按下空格以退出...')
        keyboard.wait('space')
        exit(0)
    console.clear()
    verify_space = Verify('Tidy terminal 的安装大约需要您的系统磁盘拥有xx MB 的空间, 请保持系统磁盘空间容量充足.')
