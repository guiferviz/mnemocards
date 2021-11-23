
import os
import sys

from anki.collection import Collection
from anki.importing.apkg import AnkiPackageImporter

from mnemocards.utils import create_check_collection_path


def import_command(apkgs, collection_path=None, profile=None):
    # Get an existing collection path. Error if not exists.
    collection_path = create_check_collection_path(collection_path, profile)
    # I need to do this because creating a collection changes the current path.
    # Anki should fix that I think...
    apkgs = [os.path.abspath(i) for i in apkgs]
    # Create collection.
    col = Collection(collection_path)
    # Import collection.
    for a in apkgs:
        AnkiPackageImporter(col, a).run()
    # Close collection.
    col.close()

