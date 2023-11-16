import hashlib
import subprocess
from concurrent.futures import ThreadPoolExecutor
from functools import partial
from threading import Event
from typing import Iterable
from urllib.request import urlopen
from git.repo import Repo

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


def up(title, options: list):
    global n_select, a
    if a == 0:
        if n_select > 0:
            n_select -= 1
        console.clear()
        console.print(title, justify='center')
        for l, c in zip(range(len(options)), options):
            if l == n_select:
                console.print(f'{l + 1}. {c}', justify='center', style='#FF9933')
            else:
                console.print(f'{l + 1}. {c}', justify='center')


def down(title, options: list):
    global n_select, a
    if a == 0:
        if n_select >= 0 and n_select < len(options) - 1:
            n_select += 1

        console.clear()
        console.print(title, justify='center')
        for l, c in zip(range(len(options)), options):
            if l == n_select:
                console.print(f'{l + 1}. {c}', justify='center', style='#FF9933')
            else:
                console.print(f'{l + 1}. {c}', justify='center')


def select(title: str, options: list):
    global n_select, a
    a = 0
    n_select = 0
    console.clear()
    console.print(title, justify='center')
    for l, c in zip(range(len(options)), options):
        if l == n_select:
            console.print(f'{l + 1}. {c}', justify='center', style='#FF9933')
        else:
            console.print(f'{l + 1}. {c}', justify='center')
    keyboard.add_hotkey('up', up, args=(title, options,), suppress=True)
    keyboard.add_hotkey('down', down, args=(title, options,), suppress=True)
    keyboard.wait('enter', True)
    a = 1
    return n_select


console.clear()
console.print('')

console.clear()
console.print('You are welcome to install the boot program using Tidy terminal!', style='magenta', justify='center')
console.print('(Please press [blue]Enter[/] to enter the installation)', justify='center')
keyboard.wait('enter', True)

install_select = select('Do you have python 3.11?', ['Yes', "No, I don't have python3.11"])
l = -1
disk_list = []
if install_select == 0:
    for c in string.ascii_uppercase:
        disk = c + ':'
        if os.path.isdir(disk):
            l += 1
            disk_list.append(disk)
            if os.path.exists(
                    f'{disk_list[l]}\\Users\\{getpass.getuser()}\\AppData\\Local\\Programs\\Python\\Python311\\python.exe'):
                python_exe = f'{disk_list[l]}\\Users\\{getpass.getuser()}\\AppData\\Local\\Programs\\Python\\Python311\\python.exe'

                python_exists = 1
                break
    if python_exists == 1:
        pass

else:
    sel_oe = select('Please select a run mode', ['Download and install the python3.11 full environment',
                                                 'Using python 3.11 embeddable package environment'])
    if sel_oe == 0:
        if file_exist('python-3.11.5-amd64.exe'):
            if sha256sum(
                    './python-3.11.5-amd64.exe') == '1bb46f65bb6f71b295801c8ff596bb5b69fa4c0645541db5f3d3bac33aa6eade':
                pass
            else:
                download('https://www.python.org/ftp/python/3.11.5/python-3.11.5-amd64.exe', './')
        else:
            download(['https://www.python.org/ftp/python/3.11.5/python-3.11.5-amd64.exe'], './')
        webbrowser.open(f'{os.getcwd()}/doc/python-install-guide-EN.html')
        console.print(
            'The installation help page has been opened in the default browser. If it is not displayed, '
            'switch to the browser manually.',
            style='#FFFF00')
        subprocess.Popen('./python-3.11.5-amd64.exe')
        with console.status("Press [blue]Enter[/] to continue.", spinner='line'):
            keyboard.wait('enter', True)
        disk_list = []
        l = -1
        python_exists = 0
        for c in string.ascii_uppercase:
            disk = c + ':'
            if os.path.isdir(disk):
                l += 1
                disk_list.append(disk)
                if os.path.exists(
                        f'{disk_list[l]}\\Users\\{getpass.getuser()}\\AppData\\Local\\Programs\\Python\\Python311\\python.exe'):
                    python_exists = 1
                    break
        p_python = f'{disk_list[l]}\\Users\\{getpass.getuser()}\\AppData\\Local\\Programs\\Python\\Python311\\python.exe'
        console.clear()
        if python_exists == 0:
            while True:
                i_r_select = select(
                    'python cannot be detected, please enter it manually or check that python is installed correctly',
                    ['Enter manually', 'Check that python is installed correctly'])
                if i_r_select == 0:
                    i_p_py = console.input('[red]python installation path> [/] ')
                    if os.path.exists(i_p_py):
                        p_python = i_p_py
                        break
                else:
                    l = -1
                    python_exists = 0
                    for c in string.ascii_uppercase:
                        disk = c + ':'
                        if os.path.isdir(disk):
                            l += 1
                            disk_list.append(disk)
                            if os.path.exists(
                                    f'{disk_list[l]}\\Users\\{getpass.getuser()}\\AppData\\Local\\Programs\\Python\\Python311\\python.exe'):
                                python_exists = 1
                                p_python = f'{disk_list[l]}\\Users\\{getpass.getuser()}\\AppData\\Local\\Programs\\Python\\Python311\\python.exe'
                                break
        while True:
            console.clear()
            with console.status("Getting in touch with the remote warehouse", spinner='line'):
                try:
                    Repo.clone_from('https://github.com/XinZhongyouxiwang/Tidy_Terminal',
                                    to_path=os.path.join('Tidy-terminal'), branch='master')
                    break
                except:
                    try:
                        Repo.clone_from('https://gitee.com/xzyxw10592191MrChen/Tidy_Terminal.git',
                                        to_path=os.path.join('Tidy-terminal'), branch='master')
                        break
                    except:
                        console.print('Unable to contact the remote repository, press enter to try again.',
                                      style='red')
                        keyboard.wait('enter', True)
        console.clear()
        console.print('The installation is complete and Tidy terminal is being initialized.')

        if file_exist(f'{os.getcwd()}\\doc'):
            remove(f'{os.getcwd()}\\doc', 'd')
        if file_exist('python-3.11.5-amd64.exe'):
            remove('./python-3.11.5-amd64.exe', 'f')
        if file_exist(f'{os.getcwd()}\\Tidy-terminal\\config\\setting.json'):
            d_json_setting = read(f'{os.getcwd()}\\Tidy-terminal\\config\\setting.json', 'json')
            d_json_setting['terminal']['root_default_path'] = os.getcwd()
            write(f'{os.getcwd()}\\Tidy-terminal\\config\\setting.json', d_json_setting, 'json')

        # 安装库
        os.system('pip install pyautogui')
        os.system('pip install')
        s_use_now = select('Tidy terminal initialization is complete, do you want to use Tidy terminal now?',
                           ['Yes', 'No'])
        if s_use_now == 0:
            os.system(f'python {os.getcwd()}\\Tidy-terminal\\Tterminal.py')
