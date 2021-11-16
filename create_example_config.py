import json


def create_example_config():
    sample_config = {
        "server_address": "127.0.0.1",
        "port": 2222,
        "username": "user",
        "password": "12345",
        "server_root": "/Data/Upload",
        "local_root": "/home/toybrick",
        "host_name": "board",
        "paths": [
            {
                "src": "lamp_sample",
                "dst": "lamp_sample"
            },
            {
                "src": "Multicast_rk",
                "dst": "other/Multicast_rk"
            },
            {
                "src": "code/lamp_detect",
                "dst": "code_lamp_detect"
            },
        ]
    }

    # s = json.dumps(sample_config)
    with open("config.json", encoding="utf8", mode="w") as f:
        # f.write(s)
        json.dump(sample_config, f, indent=2)


if __name__ == "__main__":
    create_example_config()
