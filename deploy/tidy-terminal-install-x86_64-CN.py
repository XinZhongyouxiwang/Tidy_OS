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


class NotAFileError(Exception):
    def __init__(self, message):
        self.message = message

    def __str__(self):
        return self.message


class ReadError(Exception):
    def __init__(self, message):
        self.message = message

    def __str__(self):
        return self.message


def file_exist(*path: str):
    if len(path) == 1:
        if os.path.exists(path[0]):
            return True
        else:
            return False
    elif len(path) > 1:
        return_list = []
        for i in path:
            if os.path.exists(i):
                return_list.append(True)
            else:
                return_list.append(False)
        return return_list
    else:
        return False


def isfile(*path):
    if len(path) == 1:

        if file_exist(path[0]):

            if os.path.isfile(path[0]):
                return True
            else:
                return False
        else:
            raise FileNotFoundError('file_driver.isfile: file not exist')

    elif len(path) > 1:
        return_list = []

        for i in path:

            if file_exist(i):

                if os.path.isfile(i):
                    return_list.append(True)

                else:
                    return_list.append(False)

            else:
                return_list.append(False)

        return return_list

    else:
        return False


class MakeError(Exception):
    def __init__(self, message):
        self.message = message

    def __str__(self):
        return self.message


def mkdir(path: str):
    if not file_exist(path):
        try:
            os.makedirs(path)
        except:
            raise MakeError("file_driver.mkdir: an unknown error occurred while creating the directory")
    elif file_exist(path):
        raise FileExistsError("file_driver.mkdir: path already exist")
    else:
        raise RuntimeError("file_driver.mkdir: unknown error")


def touch(path: str):
    old_path = path
    path_lest_len = path.split('/')
    path = path[0:len(path) - len(path_lest_len[-1])]

    if not file_exist(path):
        mkdir(path)
        try:
            touch_file = open(old_path, 'w')
            touch_file.write('')
            touch_file.close()
        except:
            raise MakeError("file_driver.touch: an unknown error occurred while creating the file")
    elif file_exist(path):
        if file_exist(old_path):
            pass
        else:
            try:
                touch_file = open(old_path, 'w')
                touch_file.write('')
                touch_file.close()
            except:
                raise FileExistsError("file_driver.touch: file is exist")
    else:
        raise RuntimeError("file_driver.touch: unknown error")


def read(path: str, mode: str = 'r'):
    if mode == 'r':
        if file_exist(path):
            if isfile(path):
                try:
                    read_file = open(path, 'r')
                    read_content = read_file.read()
                    read_file.close()
                    return read_content
                except:
                    raise ReadError("file_driver.read: read error")
            else:
                raise NotAFileError("file_driver.read: path is not a file")
        else:
            raise FileNotFoundError("file_driver.read: file is not exist")

    elif mode == 'rb':
        if file_exist(path):
            if isfile(path):
                try:
                    read_file = open(path, 'rb')
                    read_content = read_file.read()
                    read_file.close()
                    return read_content
                except:
                    raise ReadError("file_driver.read: read error")
            else:
                raise NotAFileError("file_driver.read: path is not a file")
        else:
            raise FileNotFoundError("file_driver.read: file is not exist")

    elif mode == 'json':
        # 读取json文件并保存为字典
        if file_exist(path):
            if isfile(path):
                try:
                    file_read = open(path, 'r')
                    # content = file_read.read()
                    return_content = json.loads(file_read.read())
                    file_read.close()
                    return dict(return_content)
                except:
                    raise ReadError("file_driver.read: json file read error")

            else:
                raise NotAFileError("file_driver.read: path is not a file")
        else:
            raise FileNotFoundError('file_driver.read: file is not exist')
    else:
        raise RuntimeError("file_driver: unknown mode")


def write(path: str, content, mode: str = 'w'):
    if mode == 'w':
        if file_exist:
            if isfile(path):
                try:
                    write_file = open(path, 'w')
                    write_file.write(content)
                    write_file.close()
                except:
                    raise RuntimeError("file_driver.write: write error")
            else:
                raise RuntimeError("file_driver.write: path is not a file")
        else:
            touch(path)
    elif mode == 'a':
        if file_exist(path):
            if isfile(path):
                try:
                    write_file = open(path, 'a')
                    write_file.write(content)
                    write_file.close()
                except:
                    raise RuntimeError("file_driver.write: write error")
            else:
                raise RuntimeError("file_driver.write: path is not a file")
        else:
            touch(path)
    elif mode == 'json':
        if file_exist(path):
            if isfile(path):
                try:
                    content = dict(content)
                except:
                    raise TypeError('file_driver.write: content must be dict')
                try:
                    write_file = open(path, 'w')
                    write_file.write(json.dumps(content))
                    write_file.close()
                except:
                    raise RuntimeError("file_driver.write: write error")
            else:
                raise NotAFileError("file_driver.write: path is not a file")
        else:
            touch(path)
    else:
        raise RuntimeError("file_driver: unknown mode")


def remove(path, mode='f'):
    if mode == 'f':
        if file_exist(path):
            if isfile(path):
                try:
                    pathlib.Path.unlink(path)
                except:

                    raise RuntimeError("file_driver.remove: remove error")
            else:
                raise RuntimeError("file_driver.remove: path is not a file")
        else:
            raise RuntimeError("file_driver.remove: file is not exist")
    elif mode == 'd':
        if file_exist(path):
            if not isfile(path):
                try:
                    shutil.rmtree(path)
                except:
                    raise RuntimeError("file_driver.remove: remove error")
            else:
                raise RuntimeError("file_driver.remove: path is not a dir")
        else:
            raise RuntimeError("file_driver.remove: dir is not exist")
    else:
        raise RuntimeError("file_driver: unknown mode")


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
    def __init__(self, title, options):
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

    def select(self):
        self.display()
        keyboard.add_hotkey('up', self.up)
        keyboard.add_hotkey('down', self.down)
        keyboard.wait('enter', True)
        return self.n_select

    def number(self):
        return self.select() + 1

    def content(self):
        return self.options[self.select()]


def exit_installer():
    console.print('正在尝试自动退出Tidy terminal 安装程序...')
    console.print('tidy-terminal-install-x86_64-CN.py:exit_installer:正在尝试清理缓存文件...')
    try:
        remove(f'{os.getcwd()}\\doc', 'd')
        remove('./python-3.11.5-amd64.exe', 'f')
    except:
        console.print('tidy-terminal-install-x86_64-CN.py:exit_installer:完成清理缓存文件!')
        console.print('等待按下 空格键 退出', style='red')
        keyboard.wait('space')
        exit(0)


class Python:
    def __init__(self, ):
        pass

    def python_exist(self):
        global python_exist
        l = -1
        disk_list = []
        self.python_exist_ = 0
        for c in string.ascii_uppercase:
            disk = c + ':'
            if os.path.isdir(disk):
                l += 1
                disk_list.append(disk)
                if os.path.exists(
                        f'{disk_list[l]}\\Users\\{getpass.getuser()}\\AppData\\Local\\Programs\\Python\\Python311\\python.exe'):
                    self.python_exe = f'{disk_list[l]}\\Users\\{getpass.getuser()}\\AppData\\Local\\Programs\\Python\\Python311\\python.exe'
                    self.python_exist_ = 1
        if self.python_exist_ == 1:
            return True
        else:
            return False

    def get_python_path(self):
        if self.python_exist():
            return self.python_exe
        else:
            return None

<<<<<<< HEAD
    def get_python_version(self):
        """
        ! 该方法会阻断主进程
        :return:
        """
        if self.python_exist():
            return os.popen(f'{self.python_exe} --V').read()[7:]


if __name__ == '__main__':
    console.print('[red]请确保已安装Python')
    console.print('按下 [blue] Enter [/]继续')
    keyboard.wait('enter')
    python_info = Python()
try:
    if python_info.get_python_path() is None:
        sel_python_path = Select(
            '请重新配置python路径\n''我们无法在您的电脑上找到Python, 请确保您的python已经安装并且相关的环境变量已部署',
            ['我已配置好相关环境变量,继续安装', '重新检测', '退出安装'])
        if sel_python_path.number() == 1:
            if python_info.python_exist():

            else:
                sel_netx_ny = .print(
                    '[red]是否继续安装?\n我们无法在您的计算机上找到Python, 请确保您的python已经安装并且相关的环境变量已部署',
                    ['继续安装', '重新检测', '退出安装'])

except:
    pass
=======
        # 安装库
        os.system('pip install pyautogui')
        os.system('pip install keyboard')
        os.system('pip install gitpython')
        os.system('pip install rich')
        os.system('pip install pywebio')
        s_use_now = Select('Tidy terminal initialization is complete, do you want to use Tidy terminal now?',
                           ['Yes', 'No'])
        if s_use_now == 0:
            os.system(f'python {os.getcwd()}\\Tidy-terminal\\Tterminal.py')
>>>>>>> redeploy
