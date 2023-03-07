from typing import Any, Dict

from mnemocards import NoteDict, PydanticTask


class SetProperty(PydanticTask):
    property_value_map: Dict[str, Any] = {}

    def process_one(self, note: NoteDict) -> NoteDict:
        for k, v in self.property_value_map.items():
            note[k] = v
        return note
