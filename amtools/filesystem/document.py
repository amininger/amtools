import os

from amtools import FileReader
from amtools.markdown.parsers import MarkdownParser

from .fsutil import fsutil
from .file import File, FileContext
from .directory import Directory

class Document(File):
    def __init__(self, path: str, context: FileContext):
        super().__init__(path, context)
        self.filename = os.path.basename(self.path)
        self.name = fsutil.filename2title(self.filename)

        self.metadata = fsutil.read_file_metadata(self.get_local_path())
        self.parent = Directory(self.dir, self.context)

        # Merge directory metadata
        for k, v in self.parent.metadata.items():
            if k not in self.metadata:
                self.metadata[k] = v

    def get_title(self) -> str:
        if 'title' in self.metadata:
            return self.metadata['title']
        return fsutil.filename2title(os.path.basename(self.path))
    
    def get_text(self) -> str:
        if os.path.exists(self.get_local_path()):
            with open(self.get_local_path(), 'r') as f:
                return f.read()
        return ""

