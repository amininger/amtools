import os

from .fsutil import fsutil
from .file_context import FileContext
from .file import File

class TextDoc(File):
    def __init__(self, path: str, context: FileContext):
        super().__init__(path, context)

        self.metadata['title'] = fsutil.filename2title(self.filename)
        metadata = fsutil.read_file_metadata(self.get_local_path())
        for k, v in metadata.items():
            self.metadata[k] = v

    def get_text(self, skip_metadata=False) -> str:
        with open(self.get_local_path(), 'r') as f:
            text = f.read()
        if skip_metadata:
            return fsutil.remove_metadata(text)
        return text

    def get_title(self) -> str:
        return self.metadata['title']

    def __str__(self):
        return self.path + ":\n" + self.get_text()
