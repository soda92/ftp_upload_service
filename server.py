import config
from pyftpdlib.authorizers import DummyAuthorizer
from pyftpdlib.handlers import FTPHandler
from pyftpdlib.servers import FTPServer

authorizer = DummyAuthorizer()
authorizer.add_user(config.username, config.password,
                    "data-server", perm="elradfmwMT")
handler = FTPHandler
handler.passive_ports = range(60000, 60010)
handler.authorizer = authorizer

server = FTPServer((config.server_addr_server, config.server_port), handler)

server.serve_forever()
