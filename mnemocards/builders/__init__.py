
from mnemocards.builders.markdown_card_builder import MarkdownCardBuilder
from mnemocards.builders.vocabulary_builder import VocabularyBuilder
from mnemocards.builders.expression_builder import ExpressionBuilder


_BUILDERS = {
    "markdown_card": MarkdownCardBuilder(),
    "language_card": VocabularyBuilder(),
    "expressions_card": ExpressionBuilder(),
}


def get_builder(builder_type):
    return _BUILDERS[builder_type]

