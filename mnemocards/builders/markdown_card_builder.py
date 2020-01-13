
import os
import re
import yaml

import genanki
import markdown2

from mnemocards import ASSETS_DIR
from mnemocards.utils import get_hash_id
from mnemocards.utils import NoteID


######################
#  Regex definition  #
######################

# Start card definition with at least 3 <: <<<
# We delete any extra white space character (including \n) between the start
# mark and the text inside the card.
START_CARD = "<{3,}\s*"
# Finish card definition with at least 3 >: >>>
# We delete any trailing space character.
END_CARD = "\s*>{3,}"

# Separate head of the card from the title from at least 3 =: ===
HEAD_SEPARATOR = "\s*={3,}\s*"
HEAD_BODY = f"(?:(?!{END_CARD}).)+?"
# Capturing only the body of the head, head not required.
HEAD = f"(?:({HEAD_BODY}){HEAD_SEPARATOR})?"
TITLE_BODY = ".+?"
# Capturing title, title required.
TITLE = f"({TITLE_BODY})"
# Separate title of the card from the body with at least 3 -: ---
BODY_SEPARATOR = "\s*-{3,}\s*"
BODY_BODY = ".+?"
# Capturing only the "body of the body", body not required.
BODY = f"(?:{BODY_SEPARATOR}({BODY_BODY}))?"

# Card regex definition.
CARD_REGEX = f"{START_CARD}{HEAD}{TITLE}{BODY}{END_CARD}"
CARD_REGEX_FLAGS = re.S


###########################
#  Anki model definition  #
###########################

css = open(f"{ASSETS_DIR}/css/markdown_github.css").read()
css += open(f"{ASSETS_DIR}/css/highlight/github.css").read()
CARD_CSS = css
CARD_MODEL = genanki.Model(
    get_hash_id("b35641cc-0e2b-4d6d-9f3d-6da338096984"),
    "Markdown-cards model",
    fields=[
        {"name": "Title"},
        {"name": "Back"},
    ],
    templates=[
        {
            "name": "Two-sides Card",
            "qfmt": '''
                <div class="title_card">{{Title}}</div>
            ''',
            "afmt": '''
                <div class="title_card">{{Title}}</div>
                <hr>
                <div class="back_card">{{Back}}</div>
            ''',
        },
    ],
    css=css,
)

#############################
#  Markdown2 configuration  #
#############################

MARKDOWN_EXTRAS = ["cuddled-lists", "fenced-code-blocks", "code-friendly"]


def find_all(text):
    return re.findall(CARD_REGEX, text, CARD_REGEX_FLAGS)


def process_math_match(match):
    eq = match.group(1)
    eq = re.sub("\\\\", "\\\\\\\\", eq)
    return f"\\\\\[{eq}\\\\\\]"


def change_mathjax_delimiters(text):
    # Inline math.
    text = re.sub("(?<![$\\\])\$([^$\\n]+?)\$", "\\\\\\(\\1\\\\\\)", text)
    # Block math.
    # FIXME: For some reason I cannot use (.+?) with re.S, it does not match
    # multiline math blocks. The current code does not allow the use of dollars
    # inside the math formulas.
    text = re.sub("\$\$\\s*([^\$]+?)\\s*\$\$", process_math_match, text)
    # Scaped dollar$.
    text = re.sub("\\\\\$", "$", text)
    return text


def process_img_match(match, data_dir, media):
    img = match.group(0)
    url = match.group(1)
    filename = os.path.join(data_dir, url)
    if not os.path.exists(filename):
        print(f"Image not found '{url}'")
        return img
    else:
        media.append(filename)
        start = match.start(1) - match.start(0)
        end = match.end(1) - match.end(0)
        basename = os.path.basename(filename)
        return img[:start] + basename + img[end:]


def search_media(text, data_dir, src):
    media = []
    #imgs = re.findall("<img +src *= *[\"'](.+?)[\"'].*?>", text)
    IMG_PATTERN = "<img +src *= *[\"'](.+?)[\"'].*?>"
    text = re.sub(IMG_PATTERN,
                  lambda match: process_img_match(match, data_dir, media),
                  text)
    return text, media


def generate_html(text, data_dir, src):
    text = change_mathjax_delimiters(text)
    text, media = search_media(text, data_dir, src)
    text = markdown2.markdown(text, extras=MARKDOWN_EXTRAS)
    return text, media


class MarkdownCardBuilder(object):

    def __init__(self):
        pass

    def build_cards(self, data_dir, src, deck_config):
        cards, media = [], []
        # Read config.
        card_properties = src.get("card_properties", None)
        tags = []
        if card_properties is not None:
            tags = card_properties.get("tags", [])
        # Read markdown file.
        filename = os.path.join(data_dir, src["file"])
        with open(filename) as file:
            text = file.read()
            cards_txt = find_all(text)
            # For each card find in the text...
            for metadata, header, body in cards_txt:
                metadata = yaml.safe_load(metadata)
                # If metadata is empty we use a default value.
                if metadata is None:
                    metadata = {}
                note_tags = tags.copy()
                note_tags.extend(metadata.get("tags", "").split(","))
                header, m = generate_html(header, data_dir, src)
                media.extend(m)
                body, m = generate_html(body, data_dir, src)
                media.extend(m)
                note_id = metadata.get("id", get_hash_id(header))
                my_note = NoteID(
                    note_id,
                    model=CARD_MODEL,
                    fields=[header, body],
                    tags=note_tags
                )
                cards.append(my_note)
        return cards, media

