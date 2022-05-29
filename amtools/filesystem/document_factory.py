import os

from .directory import Directory
from .document import Document
from .markdown_doc import MarkdownDoc

def create_document(full_path: str, rel_path=None):
    """ Given a file, creates the appropriate document wrapper and returns is
        Could be one of Directory, MarkdownDoc, or None """    
    if not os.path.exists(full_path):
        return None
    if os.path.isdir(full_path):
        return Directory(full_path, rel_path)

    ext = os.path.splitext(full_path)[1]
    if ext == ".md":
        return MarkdownDoc(full_path, rel_path)
    return None
