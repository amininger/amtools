from .markdown_element import MarkdownElement
from .inline_text import InlineText

class Hyperlink(MarkdownElement):
    def __init__(self, text: InlineText, addr :str = None, title: str = None):
        self.text = text
        self.addr = addr
        self.title = title
        if self.addr is None:
            self.addr = self.text
        if self.title is not None and self.title[0].startswith('"'):
            self.title = self.title[1:-1]

    def raw_text(self) -> str:
        return self.text.raw_text()

    def __str__(self) -> str:
        return "[" + str(self.text) + "](@" + self.addr + ")"

