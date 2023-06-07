import os

from .fsutil import fsutil
from .file_context import FileContext
from .path_object import PathObject

class Directory(PathObject):
    def __init__(self, path: str, context: FileContext):
        """ initializes the Directory object
            raises FileNotFoundException if the path is not an existing directory """
        super().__init__(path, context)

        local_dir = context.get_local(path)
        if not os.path.isdir(context.get_local(path)):
            raise FileNotFoundException(path)

        dir_file = self.context.get_local(os.path.join(self.path, '_dir.md'))
        if os.path.exists(dir_file):
            self.metadata = fsutil.read_file_metadata(dir_file)

    def get_dir(self):
        """ returns the path of the directory """
        return self.path

