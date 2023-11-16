import getpass
import os
import time

print(f'C:\\Users\\{getpass.getuser()}\\Downloads')
print(os.path.exists(f'C:\\Users\\{getpass.getuser()}\\Downloads'))