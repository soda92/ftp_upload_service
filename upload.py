import config
from ftplib import FTP

# l = []


def f(arr: list):
    def g(line):
        global s
        arr.append(line)
    return g


with FTP() as ftp:
    # ftp.debug(level=2)
    ftp.connect(host=config.server_addr, port=config.server_port)
    ftp.login(user=config.username, passwd=config.password)
    arr = []
    ftp.retrlines("LIST", callback=f(arr))
    print(arr)

# size_unused = len("drwxrwxr-x    6 1000     1000         4096 Nov 03 08:01 ")
# print(l[0][size_unused:])
