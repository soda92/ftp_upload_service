from pathlib import Path
import os
import hashlib


def get_digest(file_path):
    h = hashlib.md5()

    with open(file_path, 'rb') as file:
        while True:
            # Reading is buffered, so we can read smaller chunks.
            chunk = file.read(h.block_size)
            if not chunk:
                break
            h.update(chunk)

    return h.hexdigest()


def compare_contents(src: Path, dst: Path):
    list1,list2 = list(map(lambda x: sorted(os.listdir(str(x))), (src, dst)))
    if list1 != list2:
        return False
    for item in list1:
        p1, p2 = map(lambda x:Path.joinpath(x, item), (src, dst))
        if p1.is_file() and p2.is_file():
            hex1, hex2 = map(lambda x: get_digest(str(x)), (p1, p2))
            if hex1!=hex2:
                return False
        elif p1.is_dir() and p2.is_dir():
            if not compare_contents(p1, p2):
                return False
        else:
            return False
    return True
