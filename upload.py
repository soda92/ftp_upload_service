import os
import config
from pathlib import Path
from ftplib import FTP
import logging

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p')


def f(arr: list):
    def g(line):
        global s
        arr.append(line)
    return g


# def is_dir_exist(ftp: FTP, dirname: Path):
#     # size_unused = len(
#     #     "drwxrwxr-x    6 1000     1000         4096 Nov 03 08:01 ")
#     size_unused = 56
#     arr = []
#     ftp.retrlines(cmd="LIST", callback=f(arr))
#     names = [line[size_unused-1:] for line in arr]
#     types = [line[0] for line in arr]
#     for i in range(len(names)):
#         if types[i] == 'd':
#             if names[i] == dirname.name:
#                 return True
#     return False

# def get_filenames(ftp: FTP, dir_name: Path):
#     # size_unused = len(
#     #     "drwxrwxr-x    6 1000     1000         4096 Nov 03 08:01 ")
#     ftp.cwd(str(dir_name))
#     size_unused = 56
#     arr = []
#     ftp.retrlines(cmd="LIST", callback=f(arr))
#     names = [line[size_unused-1:] for line in arr]
#     types = [line[0] for line in arr]
#     file_names = []
#     for i in range(len(names)):
#         if types[i] == '-':
#             file_names.append(names[i])
#     return file_names


def transfer_file(srcfile: Path, destfile: Path, ftp: FTP):
    ftp.cwd(str(destfile.parent))
    logging.info(f"transfering file: {str(destfile)}")
    with open(str(srcfile), mode='rb') as fp:
        ftp.storbinary(cmd=f"STOR {srcfile.name}", fp=fp)


# def size_equal(srcfile: Path, destfile: Path, ftp: FTP):
#     ftp.cwd(str(destfile.parent))
#     size = 0
#     try:
#         ftp.retr
#         size = ftp.size(destfile.name)
#     except:
#         return False
#     finally:
#         src_file_size = os.path.getsize(str(srcfile))
#         return size == src_file_size


def transfer_folder(srcfolder: Path, destfolder: Path, ftp: FTP):
    p: Path = srcfolder
    try:
        ftp.cwd(str(destfolder))
    except:
        logging.info(f"creating directory: {str(destfolder)}")
        ftp.mkd(str(destfolder))

    for item in os.listdir(str(srcfolder)):
        x = p.joinpath(item)
        df = destfolder.joinpath(x.name)
        if x.is_dir():
            transfer_folder(x, df, ftp)
        elif x.is_file():
            # if not size_equal(x, df, ftp):
            transfer_file(x, df, ftp)


def upload():
    ftp: FTP = FTP()
    ftp.encoding = 'utf8'
    # ftp.debug(level=2)
    ftp.connect(host=config.server_addr, port=config.server_port)
    ftp.login(user=config.username, passwd=config.password)
    CURR = Path(__file__).resolve().parent
    DATA = Path.joinpath(CURR, "local-data")
    transfer_folder(DATA, Path('/'+config.host_name), ftp)
    ftp.close()


if __name__ == '__main__':
    upload()
