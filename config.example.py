from pathlib import Path
CURR_DIR = Path(__file__).resolve().parent

# host name
host_name = "test-server"

# server directory for store
server_folder = Path.joinpath(Path('/'), "upload", host_name)

# local directory to upload
local_folder = Path.joinpath(CURR_DIR, "data-local")

# server address
server_addr = "127.0.0.1"
server_port = 2222
username = "user"
password = "12345"

server_addr_server = "0.0.0.0"
