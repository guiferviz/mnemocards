
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


def generate(args):
    if not os.path.exists(args.data_dir):
        raise Exception("Data dir does not exist")
    packages = build(args)
    save_packages(packages, args.output_dir)

