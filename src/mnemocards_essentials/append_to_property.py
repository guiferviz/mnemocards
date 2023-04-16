from typing import Any, Dict

import pydantic

from mnemocards import NoteDict, PydanticTask


class AppendToProperty(PydanticTask):
    """Append an item to a property of type list.

    Provide a collection of pairs consisting of a name and its corresponding
    value, where the name represents the note property to which we wish to add
    the value.

    Configuration example:

    ```yaml
    - task: AppendToProperty
      note_property_list: value to append
      another_not_property_list: another value to append
    ```

    If the given property is not a list you will get an error.
    """

    _property_value_map: Dict[str, Any] = {}

    @pydantic.root_validator(pre=True)
    @classmethod
    def build_extra(cls, values: Dict[str, Any]) -> Dict[str, Any]:
        property_value_map: Dict[str, Any] = {}
        for field_name in list(values):
            property_value_map[field_name] = values.pop(field_name)
        values["_property_value_map"] = property_value_map
        return values

    def process_one(self, note: NoteDict) -> NoteDict:
        for k, v in self._property_value_map.items():
            value = note.get(k, [])
            value.append(v)
            note[k] = value
        return note
