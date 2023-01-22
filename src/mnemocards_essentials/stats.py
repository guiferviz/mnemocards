import time

from rich.console import Console
from rich.table import Table

from mnemocards import NoteDict, Task


class Stats(Task):
    def start(self):
        self._count = 0
        self._start = time.perf_counter()

    def process_one(self, note: NoteDict) -> NoteDict:
        self._count += 1
        return note

    def end(self):
        end = time.perf_counter() - self._start
        table = Table(
            "[bold italic]Metric", "[bold italic]Value", title="Stats"
        )
        table.add_row("[bold]Note count", str(self._count))
        table.add_row("[bold]Total time", f"{end:.3f} seconds")
        average = end / self._count if self._count != 0 else 0
        table.add_row("[bold]Average time per note", f"{average:.3f} seconds")
        Console().print(table)
