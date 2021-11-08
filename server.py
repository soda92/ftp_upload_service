import config
from pyftpdlib.authorizers import DummyAuthorizer
from pyftpdlib.handlers import FTPHandler
from pyftpdlib.servers import FTPServer

authorizer = DummyAuthorizer()
authorizer.add_user(config.username, config.password,
                    "server-data", perm="elradfmwMT")
handler = FTPHandler
handler.authorizer = authorizer

server = FTPServer((config.server_addr, config.server_port), handler)

server.serve_forever()
