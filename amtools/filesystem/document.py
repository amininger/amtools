import os

from amtools import FileReader
from amtools.markdown.parsers import MarkdownParser
from amtools.markdown.renderers import MenuRenderer

from .fsutil import fsutil
from .file import File
from .directory import Directory

class Document(File):
    def __init__(self, file_path: str, rel_path=None):
        super().__init__(file_path, rel_path)
        self.filename = os.path.basename(self.path)
        self.name = fsutil.filename2title(self.filename)

        self.metadata = fsutil.read_file_metadata(self.path)
        self.parent = Directory(self.cur_dir, self.rel_dir)

        # Merge directory metadata
        for k, v in self.parent.metadata.items():
            if k not in self.metadata:
                self.metadata[k] = v
    
