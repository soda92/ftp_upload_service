from json import JSONEncoder
import json
from model import Server, Config

server1 = Server(name="L1", host="127.0.0.1", port=2222,
                 user="user", passwd="12345")
config = Config(server=server1.__json__(),
                paths=[
                    "D:/src/ftp_upload_service/data-local/lamp_sample:/host1/lamp"],
                schedules="3:00,3:30,4:00,4:30,5:00")

# https://stackoverflow.com/a/68926979/12291425


def wrapped_default(self, obj):
    return getattr(obj.__class__, "__json__", wrapped_default.default)(obj)


wrapped_default.default = JSONEncoder().default

# apply the patch
JSONEncoder.original_default = JSONEncoder.default
JSONEncoder.default = wrapped_default

with open("model-config.json", mode='w') as f:
    json.dump(obj=config, fp=f, indent=4)

with open("model-config.json", mode='r') as f:
    conf2 = json.load(fp=f)
    conf2 = Config(**conf2)
    for path in conf2.paths:
        print(path)
