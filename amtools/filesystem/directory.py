import os

from .fsutil import fsutil
from .file_context import FileContext

class Directory:
    def __init__(self, path: str, context: FileContext):
        local_dir = context.get_local(path)
        if not os.path.exists(local_dir) or not os.path.isdir(local_dir):
            raise FileNotFoundException(path)

        self.path     = path
        self.context  = context

        self.metadata = { }
        dir_file = self.context.get_local(os.path.join(self.path, '_dir.md'))
        if os.path.exists(dir_file):
            self.metadata = fsutil.read_file_metadata(dir_file)

    def get_local_path(self):
        return self.context.get_local(self.path)

    def get_menu(self):
        menu_file = os.path.join(self.path, self.metadata.get("menu", "_menu.md"))
        menu_file = fsutil.simplify_path(menu_file)
        local_menu = self.context.get_local(menu_file)

        return menu_file if os.path.exists(local_menu) else None

    def get_title(self) -> str:
        if 'title' in self.metadata:
            return self.metadata['title']
        return fsutil.filename2title(os.path.basename(self.path))

    def __str__(self) -> str:
        return self.path
