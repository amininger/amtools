import os

from amtools import FileReader

from .file import FileContext
from .document import Document
from .fsutil import fsutil

class TextDoc(Document):
    """ A wrapper to a text document on the filesystem """

    def __init__(self, path: str, context: FileContext):
        super().__init__(path, context)

    def __str__(self):
        return self.get_text()
