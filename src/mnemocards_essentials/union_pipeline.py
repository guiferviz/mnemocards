from typing import Iterable, List, Optional

import pydantic

from mnemocards import NoteDict, PydanticTask, Task


class UnionPipeline(PydanticTask):
    name: Optional[str] = None
    steps: List[Task]

    @pydantic.validator("steps")
    @classmethod
    def validate_at_least_one_step(cls, value):
        if value is not None and not len(value):
            raise ValueError("Pipelines should have at least one step.")
        return value

    def __len__(self) -> int:
        return len(self.steps)

    def start(self):
        for i in self.steps:
            i.start()

    def process(self, notes: Iterable[NoteDict]) -> Iterable[NoteDict]:
        for i in self.steps:
            step_notes = i.process(notes)
            yield from step_notes

    def end(self):
        for i in self.steps:
            i.end()
