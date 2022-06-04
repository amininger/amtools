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

    def get_title(self) -> str:
        if 'title' in self.metadata:
            return self.metadata['title']
        return fsutil.filename2title(self.filename)

    def get_text(self) -> str:
        if os.path.exists(self.get_local_path()):
            with open(self.get_local_path(), 'r') as f:
                return f.read()
        return ""

    def parse_elements(self) -> list:
        if self.elements is None:
            self.elements = MarkdownParser.parse_file(self.get_local_path())
        return self.elements

    def __str__(self):
        return '\n'.join(map(str, self.parse_elements()))
