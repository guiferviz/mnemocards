from typing import Any, Dict

import pydantic

from mnemocards import NoteDict, PydanticTask


class AppendToProperty(PydanticTask):
    property_value_map: Dict[str, Any] = {}

    @pydantic.root_validator(pre=True)
    @classmethod
    def build_extra(cls, values: Dict[str, Any]) -> Dict[str, Any]:
        property_value_map: Dict[str, Any] = {}
        for field_name in list(values):
            property_value_map[field_name] = values.pop(field_name)
        values["property_value_map"] = property_value_map
        return values

    def process_one(self, note: NoteDict) -> NoteDict:
        for k, v in self.property_value_map.items():
            value = note.get(k, [])
            value.append(v)
            note[k] = value
        return note
