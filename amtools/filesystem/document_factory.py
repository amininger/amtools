import os

from .file_context import FileContext
from .directory import Directory
from .text_doc import TextDoc
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
    if ext == '.txt':
        return TextDoc(path, context)
    if ext == ".md":
        return MarkdownDoc(path, context)
    return None
