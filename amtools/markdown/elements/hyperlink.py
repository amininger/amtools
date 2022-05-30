from .markdown_element import MarkdownElement
from .inline_text import InlineText

class Hyperlink(MarkdownElement):
    def __init__(self, text: InlineText, addr :str):
        self.text = text
        self.addr = addr

    def raw_text(self) -> str:
        return self.text.raw_text()

    def __str__(self) -> str:
        return "[" + str(self.text) + "](@" + self.addr + ")"

