from pathlib import Path
CURR_DIR = Path(__file__).resolve().parent


# the folder name that will be created on server
host_name = "test-server"
# local directory to upload
local_dir = Path.joinpath(CURR_DIR, "data")
# local_dir = "/home/toybrick/lamp_sample"

# server directory for store
server_dir = "out"

# server address
server_addr = "127.0.0.1"
server_port = 2222
username = "user"
password = "12345"
# existing policy
# 1: skip
# 2: check-length
exist_policy = 1
