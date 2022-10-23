
from .markdown_element import MarkdownElement
from .inline_text import InlineText

class BlockQuote(MarkdownElement):
    """ A quoted block of text """

    def __init__(self, elements):
        self.elements = elements
    
    def __str__(self) -> str:
        return "| " + "\n| ".join(str(elem) for elem in self.elements)

class Callout(BlockQuote):
    """ A quoted block of text with a special heading type """

    def __init__(self, callout_type: str, title: InlineText, elements):
        super().__init__(elements)
        self.type = callout_type
        self.title = title
        if title is None:
            self.title = "Note"
    
    def __str__(self) -> str:
        return f"| {self.title}\n| " + "\n| ".join(str(elem) for elem in self.elements)

