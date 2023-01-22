import json
from enum import Enum

import pydantic
import yaml
from rich.console import Console
from rich.panel import Panel
from rich.syntax import Syntax

from mnemocards import task
from mnemocards.types import NoteDict


class PrintFormat(str, Enum):
    YAML = "yaml"
    JSON = "json"


class Print(task.Task, pydantic.BaseModel):
    format_: PrintFormat = pydantic.Field(PrintFormat.YAML, alias="format")
    sort_keys: bool = False
    _count: int = pydantic.PrivateAttr(0)

    def process_one(self, note: NoteDict) -> NoteDict:
        console = Console()
        if self.format_ == PrintFormat.YAML:
            code = yaml.dump(
                note, allow_unicode=True, sort_keys=self.sort_keys
            ).strip()
        elif self.format_ == PrintFormat.JSON:
            code = json.dumps(
                note, ensure_ascii=False, sort_keys=self.sort_keys, indent=2
            )
        else:
            raise NotImplementedError()
        pretty = Syntax(code, self.format_)
        panel = Panel.fit(pretty, title=f"Note {self._count}")
        console.print(panel)
        self._count += 1
        return note
