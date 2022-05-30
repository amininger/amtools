
from .markdown_element import MarkdownElement
from .inline_text import InlineText

class BlockQuote(MarkdownElement):
    """ A quoted block of text """

    def __init__(self):
        self.lines = []

    def add_line(self, line: InlineText) -> None:
        self.lines.append(line)
    
    def __str__(self) -> str:
        return "| " + "\n| ".join(str(line) for line in self.lines)
