import os

from .fsutil import fsutil
from .path_object import PathObject
from .directory import Directory

class File(PathObject):
    def __init__(self, path: str):
        super().__init__(path)

        self.dir      = Directory(os.path.dirname(path))

        self.filename = os.path.basename(path)
        self.ext      = os.path.splitext(self.filename)[1][1:]

        self.metadata = self.dir.metadata.copy()

    def get_title(self) -> str:
        return self.filename


