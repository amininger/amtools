import os

from .fsutil import fsutil

class PathObject:
    """ The abstract base class for a file or directory """
    def __init__(self, path: str):
        """ initializes the PathObject
            raises FileNotFoundException if the path does not exist """
        if not os.path.exists(path):
            raise FileNotFoundException(path)

        self.path     = path

        self.metadata = { }

    def get_dir(self):
        return os.path.dirname(self.path)

    def get_menu(self):
        menu_file = os.path.join(self.get_dir(), self.metadata.get("menu", "_menu.md"))
        menu_file = fsutil.simplify_path(menu_file)

        return menu_file if os.path.exists(menu_file) else None

    def get_title(self) -> str:
        if 'title' in self.metadata:
            return self.metadata['title']
        return fsutil.filename2title(os.path.basename(self.path))

