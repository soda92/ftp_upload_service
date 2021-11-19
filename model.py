class Config:
    def __init__(self, host: str, user: str, passwd: str,
                 paths: list, schedules, debug=False, port=21) -> None:
        self.host = host
        self.port = port
        self.user = user
        self.passwd = passwd
        self.paths = paths
        self.schedules = schedules
        self.debug = debug

    def __json__(self):
        return self.__dict__

    def __repr__(self):
        return str(self.__dict__)
