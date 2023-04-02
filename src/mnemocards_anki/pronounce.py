import logging
import os
import re

import pydantic
from gtts import gTTS

from mnemocards import PydanticTask
from mnemocards_anki import utils

RE_REMOVE_PAREN = re.compile(r"[\(\[].*?[\)\]]")
logger = logging.getLogger(__name__)


def remove_parentheses(text):
    return re.sub(RE_REMOVE_PAREN, "", text)


def remove_spaces(text):
    return text.replace(" ", "")


class Pronounce(PydanticTask):
    """Pronounce text in a note attribute.

    Attributes:
        language: [Two-letter
            code](https://en.wikipedia.org/wiki/List_of_ISO_639-1_codes) of the
            language to use in the pronunciation.
        attribute_to_pronounce: Note attribute to pronounce.
        append_media_file_to: Append generated media file path to a list
            attribute. This is needed for later steps that want to access the
            media files. For example, to package notes in an APKG we need to
            know where the media files are stored in order to include them in
            the APKG.
        output_dir: Output directory where generated files will be stored. This
            directory is relative to the configuration file.
    """

    language: pydantic.constr(to_lower=True)  # type: ignore
    attribute_to_pronounce: str = "language_you_learn_word"
    append_media_file_to: str = "media_files"
    append_pronunciation_to: str = ""
    output_dir: str = "./media_files"

    @pydantic.validator("append_pronunciation_to", always=True)
    def default_append_pronunciation_to(cls, value, values):
        if not value:
            return values.get("attribute_to_pronounce")
        return value

    def start(self):
        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)

    def process_one(self, note):
        to_pronounce = note[self.attribute_to_pronounce]
        # TODO: check if this is needed.
        # to_pronounce = remove_parentheses(to_pronounce)
        if self.language == "ja":
            # If you leave those spaces you get wrong pronunciations, like in
            # `スペイン 人`. Instead of `supein jin` it pronounces it as
            # `supein hito` because the kanji `人` alone is pronounced as
            # `hito`.
            to_pronounce = remove_spaces(to_pronounce)
        hash_text = utils.get_hash_id(to_pronounce, bytes=8)
        sound_file = f"{self.output_dir}/{hash_text}.mp3"
        if not os.path.exists(sound_file):
            logger.debug(
                f"Creating audio file `{sound_file}` pronouncing `{to_pronounce}`."
            )
            tts = gTTS(to_pronounce, lang=self.language)
            tts.save(sound_file)
        note[self.append_pronunciation_to] += f" [sound:{hash_text}.mp3]"
        note[self.append_media_file_to].append(sound_file)
        return note
