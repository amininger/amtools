
from .markdown_element import MarkdownElement
from .inline_text import InlineText

class BlockQuote(MarkdownElement):
    """ A quoted block of text """

    def __init__(self, elements):
        self.elements = elements
    
    def __str__(self) -> str:
        return "| " + "\n| ".join(str(elem) for elem in self.elements)
