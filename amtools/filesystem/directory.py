import os

from .fsutil import fsutil
from .file import File

class Directory(File):
    def __init__(self, dir_path: str, rel_path=None):
        super().__init__(dir_path, rel_path)
        self.cur_dir = dir_path
        self.rel_dir = rel_path

        dir_meta = fsutil.read_file_metadata(os.path.join(self.path, '_metadata.yaml'))
        if dir_meta is not None:
            self.metadata = dir_meta

