import os

from amtools.markdown.parsers import MarkdownParser

from .fsutil import fsutil
from .text_doc import TextDoc

class MarkdownDoc(TextDoc):
    """ A wrapper to a markdown document on the filesystem """

    def __init__(self, path: str):
        super().__init__(path)
        self.elements = None

    def parse_elements(self) -> list:
        if self.elements is None:
            self.elements = MarkdownParser.parse_file(self.path)
        return self.elements

    def __str__(self):
        return self.path + '\n' + '\n'.join(map(str, self.parse_elements()))
