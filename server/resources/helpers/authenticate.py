from base64 import b64encode
from os import urandom


def generate_api_key():
    random_bytes = urandom(16)
    key = b64encode(random_bytes).decode('utf-8')
    return key
