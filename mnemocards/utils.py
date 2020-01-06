
import hashlib


def get_hash_id(unicode_str):
    byte_str = str.encode(unicode_str)
    encoded = hashlib.md5(byte_str).digest()
    return int.from_bytes(encoded[:4], byteorder="big")

