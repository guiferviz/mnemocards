from markdown import markdown

from mnemocards_essentials.markdown_card_extension import (
    MnemocardsCardExtension,
)


def test_block_processor():
    html = markdown(
        """
<<<
id: 12345
another: asd
perfect: jaja
===
Title

---
Back
>>>
    """,
        extensions=[MnemocardsCardExtension()],
    )
    print(html)
