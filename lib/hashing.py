from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import serialization, hashes

import lib.helper as helper


def load_key():
    with open(helper.get_path("public_key.pem"), "rb") as f:
        public_key = serialization.load_pem_public_key(f.read())
    return public_key

def encrypt_data(public_key, data):
    encrypted_data = public_key.encrypt(
        data.encode(),
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )
    return encrypted_data




