import os

from .fsutil import fsutil
from .file import File, FileContext

class Directory(File):
    def __init__(self, path: str, context: FileContext):
        super().__init__(path, context)
        self.dir = self.path

        dir_meta = fsutil.read_file_metadata(os.path.join(self.dir, '_metadata.yaml'))
        if dir_meta is not None:
            self.metadata = dir_meta

