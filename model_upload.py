import logging
import os
import time
from ftplib import FTP
from pathlib import Path

from model import Config


def transfer_file(srcfile: Path, destfile: Path, ftp: FTP):
    ftp.cwd(str(destfile.parent))
    # logging.info(f"transfering file: {str(destfile)}")
    size_local = os.path.getsize(str(srcfile))
    try:
        size_remote = ftp.size(destfile.name)
    except:
        # size not allowed in ASCII mode
        ftp.voidcmd('TYPE I')
        try:
            size_remote = ftp.size(destfile.name)
        except:
            with open(str(srcfile), mode='rb') as fp:
                ftp.storbinary(cmd=f"STOR {srcfile.name}", fp=fp)
            return
    if size_local == size_remote:
        return
    with open(str(srcfile), mode='rb') as fp:
        ftp.storbinary(cmd=f"STOR {srcfile.name}", fp=fp)


def transfer_folder(srcfolder: Path, destfolder: Path, ftp: FTP):
    p: Path = srcfolder
    try:
        ftp.cwd(str(destfolder))
    except:
        logging.info(f"creating directory: {str(destfolder)}")
        ftp.mkd(str(destfolder))

    item_list = sorted(os.listdir(str(srcfolder)))
    len_ = len(item_list)
    for i in range(len(item_list)):
        item = item_list[i]
        x = p.joinpath(item)
        df = destfolder.joinpath(x.name)
        if x.is_dir():
            transfer_folder(x, df, ftp)
        elif x.is_file():
            logging.info(f"uploading {i+1} of {len_}: {str(item)}")
            transfer_file(x, df, ftp)


def ensure_path(server_path: Path, ftp: FTP):
    for p in reversed(list(server_path.parents)):
        try:
            ftp.cwd(str(p))
        except:
            logging.info(f"creating directory: {str(p)}")
            ftp.mkd(str(p))
    try:
        ftp.cwd(str(server_path))
    except:
        logging.info(f"creating directory: {str(server_path)}")
        ftp.mkd(str(server_path))


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
            src = ''.join(l[0], l[1])
            dest = l[2]
        else:
            src = l[0]
            dest = l[1]

        src = Path(src)
        dest = Path(dest)
        ensure_path(dest, ftp)
        transfer_folder(src, dest, ftp)

    ftp.close()
    end = time.time()
    cost = (end-start)/60
    return cost
