import os

from amtools import FileReader

from .file import FileContext, File
from .fsutil import fsutil

class HtmlDoc(File):
    """ A wrapper to a html document on the filesystem """

    def __init__(self, path: str, context: FileContext):
        super().__init__(path, context)

    def get_text(self) -> str:
        if os.path.exists(self.get_local_path()):
            with open(self.get_local_path(), 'r') as f:
                return f.read()
        return ""

    def __str__(self):
        return self.get_text()
