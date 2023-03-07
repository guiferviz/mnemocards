import hashlib
import sys


def get_hash_id(unicode_str: str, bytes: int = 4) -> int:
    byte_str = str.encode(unicode_str)
    encoded = hashlib.md5(byte_str).digest()
    return int.from_bytes(encoded[:bytes], byteorder=sys.byteorder)
