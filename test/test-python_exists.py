import getpass
import os
import string

l = -1
disk_list = []
for c in string.ascii_uppercase:
    disk = c + ':'
    if os.path.isdir(disk):
        l += 1
        disk_list.append(disk)
        if os.path.exists(
                f'{disk_list[l]}\\Users\\{getpass.getuser()}\\AppData\\Local\\Programs\\Python\\Python311\\python.exe'):
            python_exe = f'{disk_list[l]}\\Users\\{getpass.getuser()}\\AppData\\Local\\Programs\\Python\\Python311\\python.exe'
            print('python exists')