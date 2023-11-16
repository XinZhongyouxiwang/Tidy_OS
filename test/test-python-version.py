import getpass
import sys
import string
import os

print(sys.version_info >= (3, 11) and sys.version_info < (3, 12))


print()
disk_list = []
l = -1
for c in string.ascii_uppercase:
    disk = c + ':'
    if os.path.isdir(disk):
        l += 1
        disk_list.append(disk)
        print(f'{disk_list[l]}\\Users\\{getpass.getuser()}\\AppData\\Local\\Programs\\Python\\Python311\\python.exe')
        print(os.path.exists(f'{disk_list[l]}\\Users\\{getpass.getuser()}\\AppData\\Local\\Programs\\Python\\Python311\\python.exe'))