import textwrap
from pathlib import Path
from typing import Iterator, List

import typer
from emoji import emojize
from loguru import logger
from pydantic import ValidationError

from mnemocards.any2dict.any2dict import any2dict
from mnemocards.models import RecipeModel
from mnemocards.settings import Settings


def cli_print(message, *args, **kwargs):
    typer.secho(emojize(message), *args, **kwargs)


def search_and_cook_recipes(
    cards_path: Path,
    recursive: bool,
    max_recursive_level: int,
):
    cli_print(
        "Looking for recipes... :page_with_curl:",
        fg=typer.colors.WHITE,
        bold=True,
    )
    recipes = []
    recipe_paths_generator = search_recipe_paths(
        cards_path, recursive, max_recursive_level
    )
    for i, recipe_path in enumerate(recipe_paths_generator, 1):
        try:
            recipe = load_recipe(recipe_path)
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
                f"\t{i}. Valid recipe found in `{recipe_path}` :check_mark_button:",
                fg=typer.colors.GREEN,
            )
    cli_print(
        f":sparkles:  {len(recipes)} valid recipes found :sparkles:",
        fg=typer.colors.WHITE,
        bold=True,
    )


class RecipeException(Exception):
    pass


class IORecipeException(RecipeException):
    pass


class ValidationRecipeException(RecipeException):
    pass


class TypeErrorRecipeException(RecipeException):
    pass


def load_recipe(path: Path):
    assert path.exists()
    try:
        recipe_data = any2dict(str(path))
    except Exception as exception:
        logger.opt(exception=True).error(exception)
        raise IORecipeException("Error reading file") from exception
    recipe_data_type = type(recipe_data)
    if recipe_data_type != dict:
        exception = TypeErrorRecipeException(
            f"Expecting a dictionary, found `{recipe_data_type.__name__}`"
        )
        logger.opt(exception=True).error(exception)
        raise exception
    try:
        return RecipeModel(**recipe_data)
    except ValidationError as exception:
        logger.opt(exception=True).error(exception)
        raise ValidationRecipeException("Error validating data") from exception


def search_recipe_paths(
    cards_path: Path,
    recursive: bool,
    max_recursive_level: int,
) -> Iterator[Path]:
    if cards_path.is_file():
        yield cards_path
    elif cards_path.is_dir():
        recursive_level = max_recursive_level if recursive else 1
        for i in _search_recipe_paths_in_dir(cards_path, recursive_level):
            yield i
    else:
        raise Exception(
            f"weird cards_path `{cards_path}`, not file and not directory?",
        )


def _search_recipe_paths_in_dir(
    cards_dir: Path,
    recursive_level: int,
) -> Iterator[Path]:
    if recursive_level > 0:
        for i in cards_dir.iterdir():
            if i.is_dir() and not is_hidden(i):
                for i in _search_recipe_paths_in_dir(i, recursive_level - 1):
                    yield i
            elif i.is_file() and is_recipe_file(i):
                yield i


def is_hidden(path: Path) -> bool:
    return path.name.startswith(".")


def is_recipe_file(file: Path) -> bool:
    settings = Settings()
    return file.stem == settings.recipe_filename


def cook_recipes(recipes: List[Path]):
    packages = []
    for i in recipes:
        packages += cook_recipe(i)
    return packages


def cook_recipe(recipe: Path):
    packages = []
    # TODO: packages = build_packages(data_dir, config)
    return packages


def save_packages(packages, output_dir):
    pass
    # for name, p in packages:
    #    filename = os.path.join(output_dir, f"{name}.apkg")
    #    p.write_to_file(filename)


def main(
    cards_path: Path = typer.Argument(
        ".",
        help=(
            "This path is used to search for mnemocards recipes. If the path"
            " is a file, mnemocards will assume it is a recipe."
        ),
    ),
    recursive: bool = typer.Option(
        False,
        "--recursive",
        "-r",
        help=(
            "Search for mnemocards recipes also in subdirectories of the"
            " provided path."
        ),
    ),
    max_recursive_level: int = typer.Option(
        7,
        "--max-recursive-level",
        "-m",
        min=1,
        help=(
            "If the recursive flag is active, this value specifies the maximum"
            " depth level of directories to be scanned for mnemocards recipes."
        ),
    ),
):
    """Generate a package of Anki cards from text files."""

    cli_print("Hi! :waving_hand:", fg=typer.colors.GREEN, bold=True)
    search_and_cook_recipes(cards_path, recursive, max_recursive_level)
    cli_print("See you soon! :call_me_hand:", fg=typer.colors.GREEN, bold=True)


"""
import json
import os

import genanki

from mnemocards.utils import get_hash_id
from mnemocards.utils import updater
from mnemocards.builders import get_builder


def build_cards(data_dir, deck_config):
    cards, media = [], []
    for src in deck_config["src"]:
        builder = get_builder(src["type"])
        c, m = builder.build_cards(data_dir, src, deck_config)
        cards += c
        media += m
    return cards, media


def build_deck_conf(deck_config):
    conf_dict = deck_config.get("config")
    if conf_dict is not None:
        deckconf_default_name = deck_config["name"] + " (Configuration)"
        deckconf_name = conf_dict.get("name", deckconf_default_name)
        deckconf_id = conf_dict.get("id", deckconf_name)
        if type(deckconf_id) == str:
            deckconf_id = get_hash_id(deckconf_id)
        conf_dict["id"] = deckconf_id
        conf_dict["name"] = deckconf_name
        conf = genanki.DeckConf(deckconf_id, deckconf_name)
        conf.conf = updater(conf.conf, conf_dict)
        return conf


def build_deck(data_dir, deck_config):
    cards, media = build_cards(data_dir, deck_config)
    # Create deck.
    deck_name = deck_config["name"]
    deck_id = deck_config.get("id", deck_name)
    if type(deck_id) == str:
        deck_id = get_hash_id(deck_id)
    print("\tBuilding deck: ", deck_name, " ID:", deck_id)
    conf = build_deck_conf(deck_config)
    deck = genanki.Deck(
        deck_id,
        deck_name,
        conf=conf)
    for c in cards:
        deck.add_note(c)
    return deck, media


def build_decks(data_dir, package_config):
    decks, media = [], []
    for d in package_config["decks"]:
        deck, m = build_deck(data_dir, d)
        decks.append(deck)
        media += m
    return decks, media


def build_package(data_dir, package_config):
    decks, media = build_decks(data_dir, package_config)
    # Create package.
    package = genanki.Package(decks)
    package.media_files = media
    return package


def build_packages(data_dir, config):
    packages = []
    for p in config["packages"]:
        package = build_package(data_dir, p)
        packages.append((p["name"], package))
    return packages


def build_dir(data_dir, config_file):
    packages = []
    config_file = os.path.join(data_dir, config_file)
    if os.path.exists(config_file):
        print("Building", config_file)
        with open(config_file) as file:
            config = json.load(file)
            packages = build_packages(data_dir, config)
    return packages

"""
