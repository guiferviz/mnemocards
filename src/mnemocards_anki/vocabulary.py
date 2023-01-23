from typing import List, Type

from mnemocards_anki import models


class VocabularyNoteModel(models.NoteModel):
    your_language: str
    language_you_learn: str


class VocabularyNoteType(models.NoteType):
    id: str = "13ad3f26-dd7f-4fb2-ada7-e57ff3838558"
    name: str = "Vocabulary Type"
    model: Type[models.NoteModel] = VocabularyNoteModel
    css: str = ""
    card_sides: List[models.CardSides] = [
        models.CardSides(
            name="Your Language --> Language you learn",
            front="{{your_language}}",
            back="{{your_language}}: {{language_you_learn}}",
        ),
        models.CardSides(
            name="Language you learn --> Your Language",
            front="{{language_you_learn}}",
            back="{{language_you_learn}}: {{your_language}}",
        ),
    ]
