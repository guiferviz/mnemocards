from typing import List, Type

from mnemocards_anki import models


class VocabularyNote(models.Note):
    your_language_word: str
    your_language_description: str = ""
    language_you_learn_word: str
    language_you_learn_pronunciation: str = ""
    language_you_learn_description: str = ""
    color: str = "green"


class VocabularyNoteType(models.NoteType):
    id: str = "1526ae72-e75a-4c53-9845-882bca699010"
    name: str = "Vocabulary Type"
    model: Type[models.Note] = VocabularyNote
    css: str = """
        html {
            padding: 20px;
            background-color: black;
        }

        hr {
            border: 2px solid white;
        }

        .card {
            font-size: 1.7em;
            text-align: center;
            color: white;
            border-radius: 20px;
            background: #73AD21;
            padding: 15px;
            border: 5px solid white;
            font-family: Times;
        }

        .origin.word {
        }

        .destination.word {
            font-size: 1.2em;
        }

        .fonetic {
            font-style: italic;
            font-weight: bold;
            font-size: 0.75em;
        }

        .comment {
            padding-top: 10px;
            font-size: 0.6em;
        }
    """
    card_sides: List[models.CardSides] = [
        models.CardSides(
            name="Your Language --> Language you learn",
            front="""
                <style>
                    .card {
                        background: {{color}};
                    }
                </style>
                <div class="origin word">{{your_language_word}}</div>
                <div class="origin comment">{{your_language_description}}</div>
            """,
            back="""
                <style>
                    .card {
                        background: {{color}};
                    }
                </style>
                <div class="origin word">{{your_language_word}}</div>
                <div class="origin comment">{{your_language_description}}</div>
                <hr>
                <div class="destination word">{{language_you_learn_word}}</div>
                <div class="destination fonetic">{{language_you_learn_pronunciation}}</div>
                <div class="destination comment">{{language_you_learn_description}}</div>
            """,
        ),
        models.CardSides(
            name="Language you learn --> Your language",
            front="""
                <style>
                    .card {
                        background: {{color}};
                    }
                </style>
                <div class="destination word">{{language_you_learn_word}}</div>
                <div class="destination fonetic">{{language_you_learn_pronunciation}}</div>
                <div class="destination comment">{{language_you_learn_description}}</div>
            """,
            back="""
                <style>
                    .card {
                        background: {{color}};
                    }
                </style>
                <div class="destination word">{{language_you_learn_word}}</div>
                <div class="destination fonetic">{{language_you_learn_pronunciation}}</div>
                <div class="destination comment">{{language_you_learn_description}}</div>
                <hr>
                <div class="origin word">{{your_language_word}}</div>
                <div class="origin comment">{{your_language_description}}</div>
            """,
        ),
    ]
