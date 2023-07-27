
from .markdown_element import MarkdownElement
from .inline_text import InlineText

class Heading(MarkdownElement):
    """ A heading in a markdown document """

    def __init__(self, weight: str, title: InlineText, hid: str):
        self.weight = weight
        self.title  = title
        self.hid = hid

    def children(self):
        return [ self.title ]

    def __str__(self) -> str:
        return f"[H{self.weight}: {str(self.title)}]"
