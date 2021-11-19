import os
import sys

p = os.path.dirname(sys.argv[0])
print(p)


def ensure_path(server_path: str):
    if(server_path.startswith('/')):
        server_path = server_path[1:]
    arr = server_path.split('/')
    for i in range(1, len(arr)+1):
        subpath = '/'.join(arr[0:i])
        print(subpath)

ensure_path("/Upload/data")
