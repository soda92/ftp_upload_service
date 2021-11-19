import click
import threading
# https://pypi.org/project/pyftpdlib/
from pyftpdlib.authorizers import DummyAuthorizer
from pyftpdlib.handlers import FTPHandler
from pyftpdlib.servers import FTPServer

server: FTPServer

def start_server():
    global server
    authorizer = DummyAuthorizer()
    authorizer.add_user("user", "12345",
                        ".", perm="elradfmwMT")
    handler = FTPHandler
    # https://pyftpdlib.readthedocs.io/en/latest/api.html#pyftpdlib.handlers.FTPHandler.passive_ports
    handler.passive_ports = range(60000, 60010)
    handler.authorizer = authorizer

    # https://pyftpdlib.readthedocs.io/en/latest/api.html#pyftpdlib.servers.FTPServer
    server = FTPServer(
        ('0.0.0.0', 2222), handler)
    server.serve_forever()


if __name__ == "__main__":
    # https://docs.python.org/3/library/threading.html#threading.Thread
    t = threading.Thread(target=start_server, daemon=True)
    t.start()
    # https://stackoverflow.com/a/68820695/12291425
    # https://click.palletsprojects.com/en/8.0.x/
    click.getchar()
    server.close()
