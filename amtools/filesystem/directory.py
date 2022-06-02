import os

from .fsutil import fsutil
from .file import File, FileContext

class Directory(File):
    def __init__(self, path: str, context: FileContext):
        super().__init__(path, context)
        self.dir = self.path

        meta_file = self.context.get_local(os.path.join(self.dir, '_metadata.yaml'))
        dir_meta = fsutil.read_file_metadata(meta_file)
        if dir_meta is not None:
            self.metadata = dir_meta

