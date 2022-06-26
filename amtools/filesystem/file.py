import os

from .fsutil import fsutil
from .file_context import FileContext
from .directory import Directory

class File:
    def __init__(self, path: str, context: FileContext):
        local_file = context.get_local(path)
        if not os.path.exists(local_file):
            raise FileNotFoundException(path)

        self.path     = path
        self.context  = context
        self.dir      = Directory(os.path.dirname(path), self.context)

        self.filename = os.path.basename(path)
        self.ext      = os.path.splitext(self.filename)[1][1:]

        self.metadata = self.dir.metadata.copy()

    def get_local_path(self):
        return self.context.get_local(self.path)

    def get_menu(self):
        menu_file = os.path.join(self.dir.path, self.metadata.get("menu", "_menu.md"))
        menu_file = fsutil.simplify_path(menu_file)
        local_menu = self.context.get_local(menu_file)

        return menu_file if os.path.exists(local_menu) else None

    def get_title(self) -> str:
        return self.filename

    def __str__(self) -> str:
        return self.path
    
