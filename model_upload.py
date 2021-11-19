import logging
import os
import time
from ftplib import FTP
from model import Config


def transfer_file_samedir(srcfile: str, ftp: FTP):
    size_local = os.path.getsize(srcfile)
    filename = os.path.basename(srcfile)
    try:
        size_remote = ftp.size(filename)
    except:
        size_remote = -1
    if size_local != size_remote:
        with open(str(srcfile), mode='rb') as fp:
            ftp.storbinary(cmd=f"STOR {filename}", fp=fp)


def transfer_folder(srcfolder: str, ftp: FTP):
    item_list = os.listdir(srcfolder)
    file_list = sorted(
        list(filter(lambda x: os.path.isfile(os.path.join(srcfolder, x)), item_list)))
    folder_list = sorted(
        list(filter(lambda x: os.path.isdir(os.path.join(srcfolder, x)), item_list)))

    for i, file in enumerate(file_list):
        logging.info(f"uploading {i+1} of {len(file_list)}: {file}")
        transfer_file_samedir(os.path.join(srcfolder, file), ftp)

    for i, folder in enumerate(folder_list):
        try:
            ftp.cwd(folder)
        except:
            ftp.mkd(folder)
            ftp.cwd(folder)
        newsrc = os.path.join(srcfolder, folder)
        transfer_folder(newsrc, ftp)
        ftp.cwd("..")


def ensure_path(server_path: str, ftp: FTP):
    old_cwd = ftp.pwd()
    arr = server_path.split('/')
    for i in range(1, len(arr)+1):
        subpath = '/'.join(arr[0:i])
        try:
            ftp.cwd(subpath)
        except:
            logging.info(f"creating directory: {str(subpath)}")
            ftp.mkd(subpath)
    ftp.cwd(old_cwd)


def upload_using_config(config: Config) -> float:
    ftp: FTP = FTP()
    ftp.encoding = 'utf8'
    # ftp.debug(level=2)
    ftp.connect(host=config.server.host, port=config.server.port)
    ftp.login(user=config.server.user, passwd=config.server.passwd)

    start = time.time()

    for path in config.paths:
        l = path.split(":")
        if len(l) == 3:
            src = ':'.join(l[0:2])
            dest = l[2]
        else:
            src = l[0]
            dest = l[1]
        ensure_path(dest, ftp)
        ftp.cwd(dest)
        ftp.voidcmd('TYPE I')
        transfer_folder(src, ftp)

    ftp.close()
    end = time.time()
    cost = end-start
    # minutes
    cost = cost/60
    return cost
