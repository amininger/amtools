import os

from amtools import FileReader
from amtools.markdown.parsers import MarkdownParser
from amtools.markdown.renderers import make_renderer

from .document import Document
from .fsutil import fsutil

class MarkdownDoc(Document):
    """ A wrapper to a markdown document on the filesystem """

    def __init__(self, file_path: str, rel_path=None):
        super().__init__(file_path, rel_path)
        self.elements = None

    def parse(self) -> None:
        self.elements = MarkdownParser.parse_file(self.path)
        if self.elements is None:
            self.elements = []

    def get_html(self) -> str:
        if self.elements is None:
            self.parse()

        if self.rel_dir is None:
            cur_dir = self.cur_dir
        else:
            cur_dir = self.rel_dir

        renderer = make_renderer(self.metadata.get("format", "default"), cur_dir)
        return renderer.render_markdown_elements(self.elements)

    def __str__(self):
        if self.elements is None:
            self.parse()
        return '\n'.join(map(str, self.elements))
