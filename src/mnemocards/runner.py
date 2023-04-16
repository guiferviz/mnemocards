import logging
import pathlib
import textwrap
from typing import Any, Iterator, Tuple

import pydantic
import yaml
from rich.console import Console

from mnemocards import types, utils
from mnemocards.task import Task

logger = logging.getLogger(__name__)


def create_and_run_task(directory: types.PathLike, filename: str):
    directory = pathlib.Path(str(directory)).absolute()
    with utils.use_cwd(directory):
        task_config = create_task(directory, filename)
        run_task(task_config)


def read_task_config(
    directory: types.PathLike, filename: str
) -> Tuple[pathlib.Path, Any]:
    Console().print("[info]Looking for config files... :page_with_curl:")
    full_path = pathlib.Path(str(directory))
    if full_path.is_dir():
        full_path /= filename
    if not full_path.exists():
        raise FileNotFoundError(full_path)
    return full_path, yaml.safe_load(open(full_path, "r"))


def create_task(
    directory: types.PathLike,
    filename: str = "mnemocards.yaml",
    default_task: str = "mnemocards_essentials.Pipeline",
) -> Task:
    full_path, data = read_task_config(directory, filename)
    data.setdefault("type", default_task)
    task = None
    try:
        with utils.use_cwd(full_path.parent):
            task = utils.ClassModel(**data).to_object()
    except pydantic.ValidationError as e:
        error_message = e.__context__ or e
        Console().print(
            f"[error]Invalid task found in `{full_path}` :cross_mark:\n"
            + textwrap.indent(str(error_message), prefix="\t"),
        )
        raise
    else:
        Console().print(
            f"[bold green]:sparkles:  Valid task found in `{full_path}` :sparkles:",
        )
    logger.debug(
        f"Task of type `{type(task)}` created successfully from `{full_path}`."
    )
    return task


def run_task(task: Task):
    task.start()
    iterable = task.process([])
    if isinstance(iterable, Iterator):
        for _ in iterable:
            pass
    task.end()
