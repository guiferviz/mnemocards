import logging
from collections import defaultdict
from typing import Dict, List

import genanki
import pydantic

from mnemocards import NoteDict, PydanticTask
from mnemocards_anki import models
from mnemocards_anki.models import Deck, NoteType
from mnemocards_anki.utils import get_hash_id

logger = logging.getLogger(__name__)


class NoteID(genanki.Note):
    def __init__(self, note_id, **kwargs):
        super().__init__(**kwargs)
        self.note_id = note_id

    @property
    def guid(self):
        return self.note_id


class Package(PydanticTask):
    path: str = "out.apkg"
    _notes: Dict[Deck, Dict[NoteType, List[NoteDict]]] = pydantic.PrivateAttr(
        defaultdict(lambda: defaultdict(lambda: []))
    )

    def start(self):
        logger.debug("Anki packaging `start` method.")

    def process_one(self, note: NoteDict) -> NoteDict:
        logger.debug(f"Processing Anki note {note}")
        deck = note["deck"]
        note_type = note["note_type"]
        self._notes[deck][note_type] += [note]
        return note

    def end(self):
        logger.debug("Anki packaging `end` method.")
        genanki_decks: List[genanki.Deck] = []
        for deck, types2notes in self._notes.items():
            genanki_deck = genanki.Deck(deck.id, deck.name)
            for note_type, notes in types2notes.items():
                fields = [
                    i
                    for i in note_type.model.__fields__
                    if i not in models.Note.__fields__
                ]
                genanki_note_type = genanki.Model(
                    get_hash_id(note_type.id, 7),
                    note_type.name,
                    [{"name": i} for i in fields],
                    templates=[
                        {"name": i.name, "qfmt": i.front, "afmt": i.back}
                        for i in note_type.card_sides
                    ],
                    css=note_type.css,
                )
                for i in notes:
                    field_values = [i[j] for j in fields]
                    genanki_note = NoteID(
                        i["id"],
                        model=genanki_note_type,
                        fields=field_values,
                        tags=i["tags"],
                    )
                    genanki_deck.add_note(genanki_note)
            genanki_decks.append(genanki_deck)
        package = genanki.Package(genanki_decks)
        package.write_to_file(self.path)
