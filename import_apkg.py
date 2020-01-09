
import sys
from datetime import datetime

sys.path.append('/usr/share/anki')
from anki import Collection
from anki.importing.apkg import AnkiPackageImporter

profile = sys.argv[1] if len(sys.argv) > 1 else "willy"
collection_path = f"/home/guiferviz/.local/share/Anki2/{profile}/collection.anki2"
col = Collection(collection_path)
#res = col.db.list("select * from cards")

package = sys.argv[2] if len(sys.argv) > 2 else "regex"
t = datetime.now()
AnkiPackageImporter(col, f"/home/guiferviz/code/mnemocards/{package}.apkg").run()
t = datetime.now() - t

query = f"""
    select n.id
    from notes n
    left join cards c
    on c.nid = n.id
    left join (
        select did, max(n.mod) mod
        from notes n
        left join cards c
        on c.nid = n.id
        group by did
    ) d
    on d.did = c.did
    where n.mod < d.mod - {t.seconds}
"""
res = col.db.list(query)
print("Cards to remove:", res)

# Remove non-updated notes.
col.remNotes(res)

col.close()

