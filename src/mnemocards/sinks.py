from typing import Any, Dict

import yaml
from rich.console import Console
from rich.panel import Panel
from rich.syntax import Syntax

from mnemocards import utils


class Sink(utils.PydanticType):
    def __enter__(self):
        pass

    def __call__(self, note: Dict[str, Any]):
        pass

    def __exit__(self, *_):
        pass


class Print(Sink):
    def __init__(self, expand_all: bool = False):
        self.expand_all = expand_all
        self.count = 0

    def __call__(self, note: Dict[str, Any]):
        console = Console()
        yaml_code = yaml.dump(note, allow_unicode=True, sort_keys=False).strip()
        pretty = Syntax(yaml_code, "yaml")
        panel = Panel.fit(pretty, title=f"Note {self.count}")
        console.print(panel)
        self.count += 1


class Anki(Sink):
    def __init__(self):
        self.notes = []

    def __call__(self, note: Dict[str, Any]):
        self.notes.append(note)
