import hashlib
import os
import sys


def sha256sum(path):
    if not os.path.isfile(path):
        print(f'{path} is not a file')
        exit(1)
    with open(path, "rb") as f:
        sha256 = hashlib.sha256(f.read()).hexdigest()
        print(sha256, path)


if __name__ == '__main__':
    print(os.path.isdir('./'))
