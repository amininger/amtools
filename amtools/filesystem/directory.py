import os

from .fsutil import fsutil

class Directory:

    def __init__(self, dir_path: str, rel_path=None):
        self.dir_path = dir_path
        self.rel_path = rel_path

        dir_meta = fsutil.read_file_metadata(os.path.join(dir_path, '_metadata.yaml'))
        if dir_meta is not None:
            self.metadata = dir_meta
        else:
            self.metadata = { }

    def get_menu(self):
        return self.metadata.get("menu", "menu")

    def get_home(self):
        return self.metadata.get("home", "home")
