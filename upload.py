import config
from ftplib import FTP
with FTP() as ftp:
    ftp.connect(host=config.server_addr,port=config.server_port)
    ftp.login(user=config.username, passwd=config.password)
    print(ftp.retrlines("LIST"))
