
from amtools import FileReader
from amtools.markdown.parsers import MarkdownParser
from amtools.markdown.renderers import make_renderer

from .fsutil import fsutil
from .document import Document

class MarkdownDoc(Document):
    """ A wrapper to a markdown document on the filesystem """

    def __init__(self, filename: str, rel_path=None):
        super().__init__(filename, rel_path)
        self.elements = None

    def parse(self) -> None:
        self.elements = MarkdownParser.parse_file(self.filename)
        if self.elements is None:
            self.elements = []

    def get_html(self) -> str:
        if self.elements is None:
            self.parse()
        renderer = make_renderer(self.metadata.get("format", "default"))
        return renderer.render_markdown_elements(self.elements)

    def __str__(self):
        if self.elements is None:
            self.parse()
        return '\n'.join(map(str, self.elements))
