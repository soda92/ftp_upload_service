# %%
import config
from ftplib import FTP
ftp = FTP(source_address=(config.server_addr, config.server_port))

# %%
ftp.login(user=config.username, passwd=config.password)


# %%
