
from .inline_text import InlineText

class BulletedList:
    """ A bulleted list in the document, each line starts with * or - """

    def __init__(self, items: list[InlineText]):
        self.items = items

    def __str__(self) -> str:
        return '* ' + '\n* '.join(map(str, self.items))
