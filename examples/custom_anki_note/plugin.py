from enum import Enum
from typing import List, Type

import pydantic

from mnemocards_anki import models


class Toxicity(str, Enum):
    baja = "Baja"
    media = "Media"
    alta = "Alta"
    en_revision = "En revisión"


TOXICITY_TO_COLOR = {
    Toxicity.baja: "#00b300",
    Toxicity.media: "#e6cc00",
    Toxicity.alta: "#e60000",
    Toxicity.en_revision: "gray",
}


class AdditiveNote(models.Note):
    id: str = ""
    code: str
    name: str
    toxicity: Toxicity
    color: str = ""

    @pydantic.root_validator()
    @classmethod
    def default_id(cls, values):
        code = values.get("code")
        id_ = values.get("id")
        if code and not id_:
            values["id"] = f"additive-{code.lower()}"
        return values

    @pydantic.validator("color", always=True)
    @classmethod
    def default_color_based_on_toxicity(cls, value, values):
        toxicity = values.get("toxicity")
        if not value and toxicity:
            value = TOXICITY_TO_COLOR[toxicity]
        return value


class AdditiveNoteType(models.NoteType):
    id: str = "d64c9164-6d1d-4bcd-8b3d-010616cd8468"
    name: str = "Additive Type"
    model: Type[models.Note] = AdditiveNote
    css: str = """
        html {
            background-color: black;
        }

        .code {
            padding: 1em;
            font-size: 2.5em;
            text-align: center;
        }

        .name {
            padding: 0.5em;
            font-size: 1.5em;
            text-align: center;
        }

        .toxicity {
            padding: 0.5em;
            font-size: 1.2em;
            text-align: center;
        }

        .toxicity_background {
            color: white;
            background: #a6a6a6;
        }
    """
    card_sides: List[models.CardSides] = [
        models.CardSides(
            name="Additive Code & Name --> Toxicity",
            front="""
                <div class="code">{{code}}</div>
                <div class="name">{{name}}</div>
            """,
            back="""
                <style>
                    .toxicity_background {
                        background: {{color}};
                    }
                </style>
                <div class="code toxicity_background">{{code}}</div>
                <div class="name">{{name}}</div>
                <div class="toxicity toxicity_background">Toxicidad: {{toxicity}}</div>
            """,
        ),
        models.CardSides(
            name="Additive Code & Toxicity --> Name",
            front="""
                <style>
                    .toxicity_background {
                        background: {{color}};
                    }
                </style>
                <div class="code toxicity_background">{{code}}</div>
                <div class="toxicity toxicity_background">Toxicidad: {{toxicity}}</div>
            """,
            back="""
                <style>
                    .toxicity_background {
                        background: {{color}};
                    }
                </style>
                <div class="code toxicity_background">{{code}}</div>
                <div class="name">{{name}}</div>
                <div class="toxicity toxicity_background">Toxicidad: {{toxicity}}</div>
            """,
        ),
        models.CardSides(
            name="Additive Name & Toxicity --> Code",
            front="""
                <div class="name">{{name}}</div>
            """,
            back="""
                <style>
                    .toxicity_background {
                        background: {{color}};
                    }
                </style>
                <div class="code toxicity_background">{{code}}</div>
                <div class="name">{{name}}</div>
                <div class="toxicity toxicity_background">Toxicidad: {{toxicity}}</div>
            """,
        ),
    ]
