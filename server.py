from pyftpdlib.authorizers import DummyAuthorizer
from pyftpdlib.handlers import FTPHandler
from pyftpdlib.servers import FTPServer

authorizer = DummyAuthorizer()
authorizer.add_user("user", "12345", "data", perm="elradfmwMT")
authorizer.add_anonymous("data")
handler = FTPHandler
handler.authorizer = authorizer

server = FTPServer(("", 21), handler)
# set a limit for connections
server.max_cons = 256
server.max_cons_per_ip = 5
server.serve_forever()
