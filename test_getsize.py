from ftplib import FTP

ftp: FTP = FTP()
ftp.encoding = 'utf8'
# ftp.debug(level=2)
ftp.connect(host="127.0.0.1", port=2222)
ftp.login(user="user", passwd="12345")
ftp.cwd("Data/Upload/board/code_lamp_detect/")
size_remote: int
try:
    size_remote = ftp.size("CMakeLists.txt")
except:
    ftp.voidcmd('TYPE I')
    size_remote = ftp.size("CMakeLists.txt")

print(size_remote)
