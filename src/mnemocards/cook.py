import contextlib
import itertools
import logging
import pathlib
import textwrap
from typing import List, Optional

import pydantic
from rich.console import Console

from mnemocards import readers, settings, sinks, sources, transforms, types
from mnemocards.transforms import apply_transforms

logger = logging.getLogger(__name__)


def create_and_cook_recipe(directory: types.PathLike, filename: str):
    recipe = create_recipe(directory, filename)
    if recipe:
        cook_recipe(recipe)


def create_recipe(
    directory: types.PathLike, filename: str
) -> Optional[settings.RecipeModel]:
    Console().print("[bold white]Looking for recipes... :page_with_curl:")
    full_path = pathlib.Path(str(directory))
    if full_path.is_dir():
        full_path /= filename
    if not full_path.exists():
        raise FileNotFoundError(full_path)
    reader = readers.InferReader()
    data = reader.load(full_path)
    recipe = None
    try:
        recipe = settings.RecipeModel(**data)
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


def cook_recipe(recipe: settings.RecipeModel):
    cook_ingredients(recipe.sources, recipe.transforms, recipe.sinks)


def cook_ingredients(
    sources: List[sources.Source],
    transforms: List[transforms.Transform],
    sinks: List[sinks.Sink],
):
    with contextlib.ExitStack() as stack:
        for sink in sinks:
            stack.enter_context(sink)
        for value in itertools.chain(*sources):
            transformed_value = apply_transforms(value, transforms)
            for sink in sinks:
                sink(transformed_value)


"""
def get_recipe(directory: pathlib.Path, filename: str) -> RecipeModel:
    try:
        recipe = RecipeModel.from_file(path)
    except RecipeException as e:
        error_message = e.__context__ or e
        cli_print(
            f"\t{i}. Invalid recipe found in `{recipe_path}` :cross_mark:\n"
            + textwrap.indent(str(error_message), prefix="\t\t"),
            fg=typer.colors.RED,
        )
    else:
        recipes.append(recipe)
        cli_print(
            f":sparkles: Valid recipe found in `{recipe_path}` :sparkles:",
            fg=typer.colors.GREEN,
        )
    recipes = []
    recipe_paths_generator = search_recipe_paths(
        cards_path, recursive, max_recursive_level
    )
    for i, recipe_path in enumerate(recipe_paths_generator, 1):
    if len(recipes):
        s_plural = "" if len(recipes) == 1 else "s"
        cli_print(
            f":sparkles:  {len(recipes)} valid recipe{s_plural} found :sparkles:",
            bold=True,
        )
    return recipes
"""
