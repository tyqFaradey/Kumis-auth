from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import serialization, hashes

from lib.databasing import DataBase
import lib.helper as helper
import lib.hashing as hashing

import sys, pathlib


d = DataBase()

var = sys.argv[1:]

for item in var:

    data = d.get_values_by_value(("tg_username_hash", "date"), "user_nickname", item)
    print(data)

    name = f"{item}(@){data[1]}.bin"
    path = pathlib.PurePath(helper.main_directory, "encrypted_data", name)
    with open(path, "wb") as f:
        f.write(data[0])




