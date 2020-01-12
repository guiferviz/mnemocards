
import json
import os

import genanki

from mnemocards._argument_parser import parse_args
from mnemocards.utils import get_hash_id
from mnemocards.builders import get_builder


def build_cards(data_dir, deck_config):
    cards, media = [], []
    for src in deck_config["src"]:
        builder = get_builder(src["type"])
        c, m = builder.build_cards(data_dir, src, deck_config)
        cards += c
        media += m
    return cards, media

def build_deck(data_dir, deck_config):
    cards, media = build_cards(data_dir, deck_config)
    # Create deck.
    deck_name = deck_config["name"]
    deck_id = get_hash_id(deck_name)
    deck = genanki.Deck(
        deck_id,
        deck_name)
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

def build(args):
    packages = build_dir(args.data_dir, args.config_file)
    if args.recursive:
        for root, dirs, files in os.walk(args.data_dir):
            # Ignore hidden folders.
            dirs[:] = [d for d in dirs if not d[0] == "."]
            for d in dirs:
                d = os.path.join(root, d)
                packages += build_dir(d, args.config_file)
    return packages

def save_packages(packages, output_dir):
    for name, p in packages:
        filename = os.path.join(output_dir, f"{name}.apkg")
        p.write_to_file(filename)

def main():
    args = parse_args()
    packages = build(args)
    save_packages(packages, args.output_dir)


if __name__ == "__main__":
    main()

