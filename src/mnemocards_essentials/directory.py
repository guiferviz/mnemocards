import logging
from typing import Iterable

import pydantic

from mnemocards import NoteDict, Path, PydanticTask, Task, runner

logger = logging.getLogger(__name__)


class Directory(PydanticTask):
    """Read a pipeline object from another directory.

    Attributes:
        path: Path to the root directory in which the configuration file is.
            You can also specify a different configuration name.
    """

    path: Path
    _task: Task = pydantic.PrivateAttr()

    def start(self):
        logger.debug("Directory `start` method.")
        self._task = runner.create_task(self.path)
        self._task.start()

    def process(self, notes: Iterable[NoteDict]) -> Iterable[NoteDict]:
        logger.debug("Directory `process` method.")
        return self._task.process(notes)

    def end(self):
        logger.debug("Directory `end` method.")
        self._task.end()
