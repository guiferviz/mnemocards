
from mnemocards.builders.markdown_card_builder import MarkdownCardBuilder
from mnemocards.builders.vocabulary_builder import VocabularyBuilder
from mnemocards.builders.expression_builder import ExpressionBuilder
from mnemocards.builders.autogenerate_builder import AutogenerateBuilder

_BUILDERS = {
    "markdown": MarkdownCardBuilder(),
    "vocabulary": VocabularyBuilder(),
    "expression": ExpressionBuilder(),
    "autogenerate": AutogenerateBuilder(),
}


def get_builder(builder_type):
    return _BUILDERS[builder_type]
