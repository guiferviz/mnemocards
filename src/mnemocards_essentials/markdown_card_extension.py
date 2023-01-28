import re
from xml.etree import ElementTree

from markdown.blockprocessors import BlockProcessor
from markdown.extensions import Extension


class CardBlockProcessor(BlockProcessor):
    RE_FENCE_START = re.compile(r"^<{3,}$(\n)?", re.MULTILINE)
    RE_FENCE_END = re.compile(r"(\n)?^>{3,}$", re.MULTILINE)
    RE_METADATA_END = re.compile(r"(\n)?^={3,}$", re.MULTILINE)
    RE_FRONT_END = re.compile(r"(\n)?^-{3,}$", re.MULTILINE)
    RE_SPLIT_METADATA_FRONT_BACK = re.compile(
        r"(.*)(^={3,}$)(.*)(^-{3,}$)(.*)", re.MULTILINE
    )

    def test(self, parent, block):
        return self.RE_FENCE_START.match(block)

    def run(self, parent, blocks):
        original_block = blocks[0]
        blocks[0] = self.RE_FENCE_START.sub("", blocks[0])

        for block_num, block in enumerate(blocks):
            match = self.RE_FENCE_END.search(block)
            if match:
                blocks[block_num] = self.RE_FENCE_END.sub(
                    "", block[: match.span()[0]]
                )
                blocks.insert(block_num + 1, block[match.span()[1] :])
                content = "\n\n".join(blocks[0 : block_num + 1])
                self.process_content(content)
                if not self.can_split_sections(blocks[0 : block_num + 1]):
                    return False
                e = ElementTree.SubElement(parent, "div")
                e.set("class", "mnemocards-card")
                self.split_sections(e, blocks[0 : block_num + 1])
                for _ in range(0, block_num + 1):
                    blocks.pop(0)
                return True
        blocks[0] = original_block
        return False

    def process_content(self, content):
        match = self.RE_SPLIT_METADATA_FRONT_BACK.match(content)
        if match:
            breakpoint()

    def can_split_sections(self, blocks) -> bool:
        metadata_end_index = self.find_re(blocks, self.RE_METADATA_END, 0)
        if metadata_end_index is None:
            return False
        front_end_index = self.find_re(
            blocks, self.RE_FRONT_END, metadata_end_index + 1
        )
        if front_end_index is None:
            return False
        return True

    def split_sections(self, parent, blocks):
        metadata_end_index = self.find_re(blocks, self.RE_METADATA_END, 0)
        assert metadata_end_index is not None
        front_end_index = self.find_re(
            blocks, self.RE_FRONT_END, metadata_end_index + 1
        )
        assert front_end_index is not None

        e = ElementTree.SubElement(parent, "div")
        e.set("class", "mnemocards-card__metadata")
        self.parser.parseBlocks(e, blocks[0 : metadata_end_index + 1])

        e = ElementTree.SubElement(parent, "div")
        e.set("class", "mnemocards-card__front")
        self.parser.parseBlocks(
            e, blocks[metadata_end_index + 1 : front_end_index + 1]
        )

        e = ElementTree.SubElement(parent, "div")
        e.set("class", "mnemocards-card__back")
        self.parser.parseBlocks(e, blocks[front_end_index + 1 :])

    def find_re(self, blocks, regex, start):
        for i, block in enumerate(blocks[start:], start):
            match = regex.search(block)
            if match:
                start, end = match.span()
                blocks[i] = self.RE_FENCE_END.sub("", block[:start])
                blocks.insert(i + 1, block[end:])
                return i


class MnemocardsCardExtension(Extension):
    def extendMarkdown(self, md):  # noqa: N802
        md.parser.blockprocessors.register(
            CardBlockProcessor(md.parser), "card", 175
        )


def makeExtension(*args, **kwargs):  # noqa: N802
    """Method needed to convert this module in a markdown extension."""
    return MnemocardsCardExtension(*args, **kwargs)
