import os

from .directory import Directory

from amtools import FileReader
from amtools.markdown.parsers import MarkdownParser
from amtools.markdown.renderers import MenuRenderer

from .fsutil import fsutil

class Document:
    def __init__(self, filename: str, rel_path=None):
        self.filename = filename
        self.rel_path = rel_path
        self.name = fsutil.filename2title(self.filename)

        self.metadata = fsutil.read_file_metadata(filename)
        self.parent = Directory(os.path.dirname(filename))

        # Merge directory metadata
        for k, v in self.parent.metadata.items():
            if k not in self.metadata:
                self.metadata[k] = v
    
    def get_menu_html(self):
        menu_file = self.metadata.get('menu', 'menu') + '.md'
        menu_path = os.path.join(self.parent.dir_path, menu_file)
        print("MENU")
        print(menu_file)
        print(menu_path)
        md_elements = MarkdownParser.parse_file(menu_path)
        if md_elements is None:
            return None

        renderer = MenuRenderer()
        return renderer.render_markdown_elements(md_elements)

