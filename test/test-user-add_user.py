import hashlib
import sys

from test_init import import_path, index_path, console
sys.path.append(import_path)

from terminal import file_driver

dj_user_config: dict
def add_user(username:str, password:str='', default=False):
    global dj_user_config
    if username != '':
        dj_user_config = file_driver.read(f'{index_path}/test/config/user.json', 'json')
        if username in dj_user_config:
            raise ValueError(f'user.py: 创建用户失败, 用户 {username} 已存在')

        if len(dj_user_config) == 0:
            dj_user_config[username] = [hashlib.sha256(str(password).encode('utf-8')).hexdigest(), True]
            dj_user_config['root'] = [hashlib.sha256(str(password).encode('utf-8')).hexdigest(), False]
            console.print('[yellow]W: user.py: 因为user.json内没有用户,默认用户已被替换[/]')
        else:
            if default:
                dj_user_config[username] = [hashlib.sha256(str(password).encode('utf-8')).hexdigest(), default]
            else:
                dj_user_config[username] = [hashlib.sha256(str(password).encode('utf-8')).hexdigest(), default]
        try:
            file_driver.write(f'{index_path}/test/config/user.json', dj_user_config, 'json')
        except Exception as e:
            console.print(e,f'[red]E: user.py: 创建用户失败, 写入文件失败[/]')
        console.print(f'[green]user.py: 用户 {username} 创建成功[/]')
