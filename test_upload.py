from pathlib import Path
from compare_contents import compare_contents
from upload import upload_using_config


def test_upload():
    config = {
        "server_address": "127.0.0.1",
        "port": 2222,
        "username": "user",
        "password": "12345",
        "server_root": "/Data/Upload",
        "local_root": "D:\\src\\ftp_upload_service\\data-local",
        "host_name": "local-python-client",
        "paths": [
            {
                "src": "lamp_sample",
                "dst": "lamp_sample",
            },
            {
                "src": "other/Multicast_rk",
                "dst": "Multicast_rk",
            },
        ]
    }
    upload_using_config(config)
    result = True
    for dct in config["paths"]:
        src = dct["src"]
        dst = dct["dst"]
        SRC = Path(config["local_root"]).joinpath(src)
        DST = Path(
            "D:/src/ftp_upload_service/data-server").joinpath(
                str(config["server_root"])[1:],
                config["host_name"], dst)
        result1 = compare_contents(SRC, DST)
        result = result and result1
    assert result


if __name__ == "__main__":
    test_upload()
