import os

from amtools import FileReader
from amtools.markdown.parsers import MarkdownParser

from .file import FileContext
from .document import Document
from .fsutil import fsutil

class MarkdownDoc(Document):
    """ A wrapper to a markdown document on the filesystem """

    def __init__(self, path: str, context: FileContext):
        super().__init__(path, context)
        self.elements = None

    def parse(self) -> None:
        self.elements = MarkdownParser.parse_file(self.get_local_path())
        if self.elements is None:
            self.elements = []

    def __str__(self):
        if self.elements is None:
            self.parse()
        return '\n'.join(map(str, self.elements))
