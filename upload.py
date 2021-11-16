import json
import logging
import os
import sys
import time
from ftplib import FTP
from pathlib import Path

import config
from create_example_config import create_example_config

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p')


def f(arr: list):
    def g(line):
        arr.append(line)
    return g


def getsize(s: bytes):
    def g(data: bytes):
        nonlocal s
        s += data
    return g


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


def upload_using_config(config):
    config["local_root"] = Path(config["local_root"])
    config["server_root"] = Path(config["server_root"])
    ftp: FTP = FTP()
    ftp.encoding = 'utf8'
    # ftp.debug(level=2)
    ftp.connect(host=config["server_address"], port=config["port"])
    ftp.login(user=config["username"], passwd=config["password"])

    server_path = Path.joinpath(config["server_root"], config["host_name"])
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
    start = time.time()
    # upload()
    for dct in config["paths"]:
        src = dct["src"]
        dst = dct["dst"]
        local = Path.joinpath(config["local_root"], src)
        remote = Path.joinpath(config["server_root"], config["host_name"], dst)
        transfer_folder(local, remote, ftp)

    ftp.close()
    end = time.time()
    cost = (end-start)/60
    return cost


if __name__ == "__main__":
    HOME = Path(sys.argv[0]).resolve().parent
    CONFIG = Path.joinpath(HOME, "config.json")
    if not CONFIG.exists():
        logging.info("creating example config")
        create_example_config()
        sys.exit(0)
    config = ""
    with open(str(CONFIG), encoding="utf8", mode="r") as f:
        config = json.load(f)

    cost = upload_using_config(config)
    logging.info(f"total transfer time: {cost:.2f}min")
