
import json
import os
import hashlib
import uuid
import collections.abc

import genanki

from mnemocards import ASSETS_DIR


CONFIG_FILENAME = ".mnemocards"


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


def generate_card_uuid(string=None):
    if string == None:
        print(uuid.uuid4())
        return

    seed = hashlib.md5(string.encode('utf-8'))
    # seed.update(str.encode(unicode_str))
    return uuid.UUID(seed.hexdigest())


def read_asset(relative_path):
    filename = os.path.join(ASSETS_DIR, relative_path)
    with open(filename) as file:
        return file.read()


def read_config():
    filename = os.path.join(os.path.expanduser("~"), CONFIG_FILENAME)
    if os.path.exists(filename):
        with open(filename) as file:
            return json.load(file)
    return {}


def write_config(data):
    filename = os.path.join(os.path.expanduser("~"), CONFIG_FILENAME)
    with open(filename, "w") as file:
        json.dump(data, file, indent=4)


def create_check_collection_path(collection_path, profile):
    """Create from profile and check the collection path.

    If you only provide the profile, the collection path is expected to be
    in '~/.local/share/Anki2/{profile}/collection.anki2'.
    If the collection_path is given only a checking that it exists is done.
    """

    if collection_path is None and profile is None:
        raise Exception("Specify at least the collection or the profile")
    if profile is not None:
        collection_path = f"~/.local/share/Anki2/{profile}/collection.anki2"
        collection_path = os.path.expanduser(collection_path)
    # collection_path must have value here.
    if not os.path.exists(collection_path):
        raise Exception(f"Collection '{collection_path}' does not exist")
    return collection_path


def updater(old, new):
    """Recursively update a dict. """

    for k, v in new.items():
        if type(v) == dict:
            old[k] = updater(old.get(k, {}), v)
        else:
            old[k] = v
    return old
