import os
import config
from pathlib import Path
from ftplib import FTP


def f(arr: list):
    def g(line):
        global s
        arr.append(line)
    return g


def is_dir_exist(ftp: FTP, dirname: str):
    # size_unused = len(
    #     "drwxrwxr-x    6 1000     1000         4096 Nov 03 08:01 ")
    size_unused = 56
    arr = []
    ftp.retrlines(cmd="LIST", callback=f(arr))
    names = [line[size_unused:] for line in arr]
    types = [line[0] for line in arr]
    for i in range(len(names)):
        if types[i] == 'd':
            if names[i] == dirname:
                return True
    return False


def transfer_folder(srcfolder: Path, destfolder: Path, ftp: FTP):
    p: Path = srcfolder
    ftp.cwd(str(destfolder))
    for item in os.listdir(str(srcfolder)):
        x = p.joinpath(item)
        if x.is_dir():
            if not is_dir_exist(ftp, x.name):
                ftp.mkd(x.name)
                df = destfolder.joinpath(x.name)
                transfer_folder(x, df, ftp)
        elif x.is_file():
            ftp.storbinary("STOR " + x.name)
        else:
            pass


def upload():
    with FTP() as ftp:
        ftp.debug(level=2)
        ftp.connect(host=config.server_addr, port=config.server_port)
        ftp.login(user=config.username, passwd=config.password)
        CURR = Path(__file__).resolve().parent
        DATA = Path.joinpath(CURR, "local-data")
        transfer_folder(DATA, config.host_name)


if __name__ == '__main__':
    upload()
