
from .markdown_element import MarkdownElement
from .inline_text import InlineText

class Heading(MarkdownElement):
    """ A heading in a markdown document """

    def __init__(self, weight: int, title: InlineText):
        self.weight = weight
        self.title  = title

    def __str__(self) -> str:
        return f"[H{self.weight}: {str(self.title)}]"
