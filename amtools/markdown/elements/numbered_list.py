from typing import List 

from .markdown_element import MarkdownElement
from .inline_text import InlineText

class NumberedList(MarkdownElement):
    """ A numbered list in the document, each line starts with 1. """

    def __init__(self, items: List[InlineText]):
        self.items = items

    def __str__(self) -> str:
        return '1. ' + '\n* '.join(map(str, self.items))

