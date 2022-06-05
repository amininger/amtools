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

    def get_format(self) -> str:
        return self.metadata.get("format", "default")

    def parse_elements(self) -> list:
        if self.elements is None:
            self.elements = MarkdownParser.parse_file(self.get_local_path())
        return self.elements

    def __str__(self):
        return '\n'.join(map(str, self.parse_elements()))
