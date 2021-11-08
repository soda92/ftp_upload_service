import os
import config
from pathlib import Path
from ftplib import FTP
import logging
import time

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p')


def f(arr: list):
    def g(line):
        global s
        arr.append(line)
    return g


def transfer_file(srcfile: Path, destfile: Path, ftp: FTP):
    ftp.cwd(str(destfile.parent))
    logging.info(f"transfering file: {str(destfile)}")
    with open(str(srcfile), mode='rb') as fp:
        ftp.storbinary(cmd=f"STOR {srcfile.name}", fp=fp)


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
    start = time.time()
    upload()
    end = time.time()
    cost = (end-start)/60
    logging.info(f"total transfer time: {cost:.2f}min")
