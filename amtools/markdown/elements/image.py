from .markdown_element import MarkdownElement

class Image(MarkdownElement):
    def __init__(self, filename: str, alt_text: str, width: str):
        self.filename = filename
        self.alt_text = alt_text
        self.width = width

    def __str__(self) -> str:
        return "-----------IMAGE-----------\n     " + self.filename + "     \n-------------------------"

