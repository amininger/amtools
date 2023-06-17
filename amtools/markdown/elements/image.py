from .markdown_element import MarkdownElement
from .inline_text import InlineText
import re

re_ALL_DIGITS = re.compile("^\d+$")

class Image(MarkdownElement):
    def __init__(self, alt_text:str, filename:str, title: str):
        self.alt_text = alt_text
        self.filename = filename
        self.title = title

        self.width = None
        if "|" in self.alt_text:
            self.alt_text, self.width = self.alt_text.split("|")
    
    def get_css_width(self):
        if self.width is None:
            return ""
        if re_ALL_DIGITS.match(self.width):
            return self.width + "px"
        return self.width

    def __str__(self) -> str:
        return f'IMG[{self.filename}]'

class LinkedImage(Image):
    def __init__(self, alt_text:str, filename:str, title: str, addr: str):
        super().__init__(alt_text, filename, title)
        self.addr = addr

    def __str__(self) -> str:
        return f'IMG[{self.filename}] -> @{self.addr}'

