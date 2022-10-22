from typing import List 
from enum import Enum

from .markdown_element import MarkdownElement
from .inline_text import InlineText

class ListType(Enum):
    ORDERED = 1
    UNORDERED = 2

class ListItem(MarkdownElement):
    def __init__(self, list_type: ListType, text: InlineText):
        self.list_type = list_type
        self.text = text

    def __str__(self) -> str:
        symbol = ("1." if self.list_type == ListType.ORDERED else "-")
        return f'{symbol} {self.text}'

class ListBlock(MarkdownElement):
    """ A list in the document (bulleted or numbered) """

    def __init__(self, list_type: ListType, elements: List[MarkdownElement]):
        self.list_type = list_type
        self.elements = elements

    def __str__(self) -> str:
        return '\n'.join(map(str, self.elements))

