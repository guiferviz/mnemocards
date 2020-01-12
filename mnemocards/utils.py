
import hashlib

import genanki


class NoteID(genanki.Note):

    def __init__(self, note_id, **kwargs):
        super().__init__(**kwargs)
        self.note_id = note_id

    @property
    def guid(self):
        return self.note_id


def get_hash_id(unicode_str, bytes=4):
    byte_str = str.encode(unicode_str)
    encoded = hashlib.md5(byte_str).digest()
    return int.from_bytes(encoded[:bytes], byteorder="big")

