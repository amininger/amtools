from typing import List 

from .markdown_element import MarkdownElement
from .inline_text import InlineText

class BulletedList(MarkdownElement):
    """ A bulleted list in the document, each line starts with * or - """

    def __init__(self, items):
        self.items = items

    def __str__(self) -> str:
        return '\n'.join(f"{'  '*indent}* {str(text)}" for text, indent in self.items)
