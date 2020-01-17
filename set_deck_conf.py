
import sys
import json
from datetime import datetime

sys.path.append('/usr/share/anki')
from anki import Collection
from anki.importing.apkg import AnkiPackageImporter
from anki.decks import defaultConf as DEFAULT_CONF
from anki.decks import DeckManager


print(json.dumps(DEFAULT_CONF))
conf = DEFAULT_CONF.copy()
conf["new"]["initialFactor"] = 3500
conf_name = "MyConf"
conf["name"] = conf_name
deck_name = "English"

profile = sys.argv[1] if len(sys.argv) > 1 else "willy"
collection_path = f"/home/guiferviz/.local/share/Anki2/{profile}/collection.anki2"
collection_path = f"/home/guiferviz/code/mnemocards/packages/english/collection.anki2"
col = Collection(collection_path)

# Create or update config.
dm = col.decks
all_conf = dm.allConf()
conf_id = None
for c in all_conf:
    if conf["name"] == c["name"]:
        conf_id = c["id"]
if conf_id is not None:
    conf["id"] = conf_id
    dm.updateConf(conf)
    print("Updating existing conf:", conf_id)
else:
    conf_id = dm.confId(conf_name, conf)
    print("New conf added:", conf_id)

# Set conf_id as conf of the given deck.
all_decks = dm.all()
for d in all_decks:
    if d["name"] == deck_name:
        dm.setConf(d, conf_id)
        print("Updating deck to use conf")

col.close()

