# %%
import config
from ftplib import FTP
if ':' in config.server_addr:
    addr = config.server_addr.split(':')
    host = addr[0]
    port = int(addr[1])
    ftp = FTP(source_address=(host, port))
else:
    ftp = FTP(config.server_addr)

# %%
ftp.login(user=config.username, passwd=config.password)


# %%
