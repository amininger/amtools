import os

from .fsutil import fsutil

from .directory import Directory
from .document import Document
from .markdown_doc import MarkdownDoc

def create_document(filename: str, rel_path :str):
    """ Given a file, creates the appropriate document wrapper and returns is
        Could be one of Directory, MarkdownDoc, or None """    
    if not os.path.exists(filename):
        return None
    if os.path.isdir(filename):
        return Directory(filename, rel_path)

    ext = os.path.splitext(filename)[1]
    if ext == ".md":
        return MarkdownDoc(filename, rel_path)
    return None