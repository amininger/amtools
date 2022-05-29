import os

from amtools.markdown.parsers import MarkdownParser
from amtools.markdown.renderers import MenuRenderer

from .fsutil import fsutil

class File:
    def __init__(self, path: str, rel_path=None):
        self.path     = path
        self.cur_dir  = os.path.dirname(path)
        self.rel_path = rel_path
        self.rel_dir  = None if rel_path is None else os.path.dirname(rel_path)
        self.metadata = { }

    def get_home(self):
        return self.metadata.get("home", "home")

    def get_menu(self):
        return self.metadata.get("menu", "menu")

    def get_menu_html(self):
        menu_file = self.get_menu() + '.md'
        menu_path = os.path.join(self.cur_dir, menu_file)
        md_elements = MarkdownParser.parse_file(menu_path)
        if md_elements is None:
            return None

        if self.rel_dir is None:
            menu_dir = os.path.dirname(menu_path)
        else:
            menu_dir = os.path.dirname(os.path.join(self.rel_dir, menu_file))

        menu_dir = fsutil.simplify_path(menu_dir)
        renderer = MenuRenderer(menu_dir)
        return renderer.render_markdown_elements(md_elements)

