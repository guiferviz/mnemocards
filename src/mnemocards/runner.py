import logging
import pathlib
import textwrap
from typing import Optional

import pydantic
from rich.console import Console

import mnemocards_essentials as essentials
from mnemocards import types
from mnemocards.task import Task

logger = logging.getLogger(__name__)


def create_and_run_task(directory: types.PathLike, filename: str):
    recipe = create_task(directory, filename)
    if recipe:
        run_task(recipe)


def create_task(directory: types.PathLike, filename: str) -> Optional[Task]:
    Console().print("[bold white]Looking for recipes... :page_with_curl:")
    full_path = pathlib.Path(str(directory))
    if full_path.is_dir():
        full_path /= filename
    if not full_path.exists():
        raise FileNotFoundError(full_path)
    reader = essentials.readers.InferReader()
    data = reader.load(full_path)
    recipe = None
    try:
        recipe = essentials.Pipeline(**data)
    except pydantic.ValidationError as e:
        error_message = e.__context__ or e
        Console().print(
            f"[bold red]Invalid recipe found in `{full_path}` :cross_mark:\n"
            + textwrap.indent(str(error_message), prefix="\t"),
        )
        logger.exception(error_message)
    else:
        Console().print(
            f"[bold green]:sparkles:  Valid recipe found in `{full_path}` :sparkles:",
        )
    return recipe


def run_task(task: Task):
    task.start()
    iterable = task.process([])
    for _ in iterable:
        pass
    task.end()
