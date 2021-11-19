import sys
import os
import json
from model import Server, Config
from json import JSONEncoder

# https://stackoverflow.com/a/68926979/12291425


def wrapped_default(self, obj):
    return getattr(obj.__class__, "__json__", wrapped_default.default)(obj)


wrapped_default.default = JSONEncoder().default

# apply the patch
JSONEncoder.original_default = JSONEncoder.default
JSONEncoder.default = wrapped_default


def create_example():
    server1 = Server(name="L1", host="127.0.0.1", port=21,
                     user="user", passwd="12345")
    config = Config(server=server1.__json__(),
                    paths=[
                        "D:/src/ftp_upload_service/data-local/lamp_sample:/host1/lamp"],
                    schedules="3:00,3:30,4:00,4:30,5:00",
                    debug=True)

    with open("model-config.json", mode='w') as f:
        json.dump(obj=config, fp=f, indent=4)


def exists():
    p = os.path.dirname(sys.argv[0])
    file = os.path.join(p, "model-config.json")
    return os.path.isfile(file)


def read_conf():
    with open("model-config.json", mode='r') as f:
        conf2 = json.load(fp=f)
        conf2 = Config(**conf2)
        return conf2
