import os

from .directory import Directory
from .text_doc import TextDoc
from .markdown_doc import MarkdownDoc

def create_document(path: str):
    """ Given a file, creates the appropriate document wrapper and returns is
        Could be one of Directory, MarkdownDoc, or None """    
    if not os.path.exists(path):
        return None
    if os.path.isdir(path):
        return Directory(path)

    ext = os.path.splitext(path)[1]
    if ext == '.txt':
        return TextDoc(path)
    if ext == ".md":
        return MarkdownDoc(path)
    return None
