import os

from amtools.markdown.parsers import MarkdownParser

from .fsutil import fsutil

class FileContext:
    def __init__(self, working_dir: str='', url_path: str='/', media_path: str='/media'):
        """ File paths are relative to some root directory
            A FileContext contains different options for the root path
            working_dir : An absolute filesystem path to the root directory
            url_path    : A path prefix for resolving website links
            media_path  : A path prefix for media queries """

        self.working_dir = working_dir
        self.url_path    = url_path
        self.media_path  = media_path

    def get_local(self, path: str) -> str:
        return fsutil.simplify_path(os.path.join(self.working_dir, path))

    def get_url(self, path: str) -> str:
        return fsutil.simplify_path(os.path.join(self.url_path, path))

    def get_media_url(self, path: str) -> str:
        return fsutil.simplify_path(os.path.join(self.media_path, path))

    def push_dir(self, dir_path: str):
        return FileContext(os.path.join(self.working_dir, dir_path), 
                            os.path.join(self.url_path, dir_path),
                            os.path.join(self.media_path, dir_path))

class File:
    def __init__(self, path: str, context: FileContext):
        self.path     = path
        self.dir      = os.path.dirname(path)
        self.context  = context
        self.metadata = { }

    def get_local_path(self):
        return self.context.get_local(self.path)

    def get_home(self):
        home_file = os.path.join(self.dir, self.metadata.get("home", "home.md"))
        return fsutil.simplify_path(home_file)

    def get_menu(self):
        menu_file = os.path.join(self.dir, self.metadata.get("menu", "menu.md"))
        return fsutil.simplify_path(menu_file)
