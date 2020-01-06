
import os
import re

from ..utils import get_hash_id


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

css = open("css/markdown_github.css").read()
css += open("css/highlight/github.css").read()
CARD_CSS = css
CARD_MODEL = genanki.Model(
    "b35641cc-0e2b-4d6d-9f3d-6da338096984",
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


def find_all(text):
    print(CARD_REGEX)
    return re.findall(CARD_REGEX, text, CARD_REGEX_FLAGS)


class MyNote(genanki.Note):

    def __init__(self, note_id, **kwargs):
        super().__init__(**kwargs)
        self.note_id = note_id

    @property
    def guid(self):
        return genanki.guid_for(self.note_id)


class MarkdownCardBuilder(object):

    def __init__(self):
        pass

    def build_cards(self, data_dir, src, deck_config):
        cards = []
        filename = os.path.join(data_dir, src["file"])
        with open(filename) as file:
            text = file.read()
            cards_txt = find_all(text)
            for metadata, header, body in cards_txt:
                header = markdown2.markdown(header,
                                            extras=["fenced-code-blocks"])
                body = markdown2.markdown(body,
                                          extras=["fenced-code-blocks"])
                note_id = get_hash_id(header)
                my_note = MyNote(
                    note_id,
                    model=CARD_MODEL,
                    fields=[header, body],
                    tags=""
                )
        return cards

