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
