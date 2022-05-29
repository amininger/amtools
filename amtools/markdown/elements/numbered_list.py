
from .inline_text import InlineText

class NumberedList:
    """ A numbered list in the document, each line starts with 1. """

    def __init__(self, items: list[InlineText]):
        self.items = items

    def __str__(self) -> str:
        return '1. ' + '\n* '.join(map(str, self.items))

