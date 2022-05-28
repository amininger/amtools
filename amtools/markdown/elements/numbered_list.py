
class NumberedList:
    """ A numbered list in the document, each line starts with 1. """

    def __init__(self, items: list):
        self.items = items

    def __str__(self) -> str:
        return '1. ' + '\n* '.join(self.items)

