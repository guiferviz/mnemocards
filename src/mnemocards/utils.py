import importlib
from typing import Any, Dict, Optional, Union

import pydantic


class PydanticType:
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, value: Union[str, Dict[str, Any]]):
        if not isinstance(value, cls):
            if isinstance(value, str):
                value = {"type": value}
            value = ClassModel(**value).to_object()
        return value


class ClassModel(pydantic.BaseModel):
    type_: str = pydantic.Field(alias="type")
    params: Dict[str, Any]

    # Taken from:
    # https://stackoverflow.com/questions/69617489/can-i-get-incoming-extra-fields-from-pydantic
    @pydantic.root_validator(pre=True)
    @classmethod
    def build_extra(cls, values: Dict[str, Any]) -> Dict[str, Any]:
        all_required_field_names = {
            field.alias
            for field in cls.__fields__.values()
            if field.alias != "params"
        }
        params: Dict[str, Any] = {}
        for field_name in list(values):
            if field_name not in all_required_field_names:
                params[field_name] = values.pop(field_name)
        values["params"] = params
        return values

    @pydantic.validator("type_")
    @classmethod
    def validate_type_exists(cls, type_):
        if type_ is not None:
            try:
                member_from_qualified_name(
                    type_, default_module="mnemocards_essentials"
                )
            except (AttributeError, ImportError):
                raise ValueError(f"`{type_}` not found or errors during import")
        return type_

    def to_object(self):
        member = member_from_qualified_name(
            self.type_, default_module="mnemocards_essentials"
        )
        return member(**self.params)


def get_module_member(module_name: str, member_name: str) -> Any:
    m = importlib.import_module(module_name)
    return getattr(m, member_name)


def member_from_qualified_name(name: str, default_module: Optional[str] = None):
    if "." not in name:
        if default_module:
            name = f"{default_module}.{name}"
        else:
            raise ImportError(
                f"`{name}` is not a qualified name: module missing."
            )
    module_name, member_name = name.rsplit(".", 1)
    return get_module_member(module_name, member_name)
