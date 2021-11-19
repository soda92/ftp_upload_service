class Server:
    def __init__(self, name: str, host: str, port: int, user: str, passwd: str):
        self.name = name
        self.host = host
        self.port = port
        self.user = user
        self.passwd = passwd

    def __json__(self):
        return self.__dict__

    def __repr__(self):
        return str(self.__dict__)


class Config:

    def __init__(self, server, paths, schedules) -> None:
        self.server = Server(**server)
        self.paths = paths
        self.schedules = schedules

    def __json__(self):
        return self.__dict__

    def __repr__(self):
        return str(self.__dict__)
