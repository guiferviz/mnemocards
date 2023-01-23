import logging
import pathlib
import textwrap
from typing import Iterator, Optional

import pydantic
from rich.console import Console

import mnemocards_essentials as essentials
from mnemocards import types, utils
from mnemocards.task import Task

logger = logging.getLogger(__name__)


def create_and_run_task(directory: types.PathLike, filename: str):
    task_config = create_task(directory, filename)
    if task_config:
        run_task(task_config)


def read_task_config(directory: types.PathLike, filename: str):
    Console().print("[bold white]Looking for config files... :page_with_curl:")
    full_path = pathlib.Path(str(directory))
    if full_path.is_dir():
        full_path /= filename
    if not full_path.exists():
        raise FileNotFoundError(full_path)
    reader = essentials.readers.InferReader()
    return full_path, reader.load(full_path)


def create_task(
    directory: types.PathLike,
    filename: str,
    default_task: str = "mnemocards_essentials.Pipeline",
) -> Optional[Task]:
    full_path, data = read_task_config(directory, filename)
    data.setdefault("type", default_task)
    task = None
    try:
        task = utils.ClassModel(**data).to_object()
    except pydantic.ValidationError as e:
        error_message = e.__context__ or e
        Console().print(
            f"[bold red]Invalid task found in `{full_path}` :cross_mark:\n"
            + textwrap.indent(str(error_message), prefix="\t"),
        )
        logger.exception(error_message)
    else:
        Console().print(
            f"[bold green]:sparkles:  Valid task found in `{full_path}` :sparkles:",
        )
    return task


def run_task(task: Task):
    task.start()
    iterable = task.process([])
    if isinstance(iterable, Iterator):
        for _ in iterable:
            pass
    task.end()
