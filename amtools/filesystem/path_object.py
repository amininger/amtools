import os

from .fsutil import fsutil
from .file_context import FileContext

class PathObject:
    """ The abstract base class for a file or directory
        given by a path relative to a FileContext """
    def __init__(self, path: str, context: FileContext):
        """ initializes the PathObject
            raises FileNotFoundException if the path does not exist """
        local_dir = context.get_local(path)
        if not os.path.exists(local_dir):
            raise FileNotFoundException(path)

        self.path     = path
        self.context  = context

        self.metadata = { }

    def get_local_path(self):
        return self.context.get_local(self.path)

    def get_dir(self):
        return os.path.dirname(self.path)

    def get_menu(self):
        menu_file = os.path.join(self.get_dir(), self.metadata.get("menu", "_menu.md"))
        menu_file = fsutil.simplify_path(menu_file)
        local_menu = self.context.get_local(menu_file)

        return menu_file if os.path.exists(local_menu) else None

    def get_title(self) -> str:
        if 'title' in self.metadata:
            return self.metadata['title']
        return fsutil.filename2title(os.path.basename(self.path))

