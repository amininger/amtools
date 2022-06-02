import os

from .file import FileContext
from .directory import Directory
from .document import Document
from .markdown_doc import MarkdownDoc

def create_document(path: str, context: FileContext):
    """ Given a file, creates the appropriate document wrapper and returns is
        Could be one of Directory, MarkdownDoc, or None """    
    full_path = context.get_local(path)
    if not os.path.exists(full_path):
        return None
    if os.path.isdir(full_path):
        return Directory(path, context)

    ext = os.path.splitext(path)[1]
    if ext == ".md":
        return MarkdownDoc(path, context)
    return None
