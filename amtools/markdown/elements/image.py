from .markdown_element import MarkdownElement
from .inline_text import InlineText

class Image(InlineText):
    def __init__(self, info: str):
        super().__init__()
        self.filename, self.alt_text, self.width = self.parse_info(info)

    def parse_info(self, info: str):
        alt_text = ""
        width = None
        if info.startswith("![["):
            filename = info[3:-2]
            alt_parts = filename.split("|")
            if len(alt_parts) == 2:
                filename, width = alt_parts
        else:
            close_br = info.index(']')
            alt_text = info[2:close_br]
            filename = info[close_br+2:-1]
            alt_parts = alt_text.split("|")
            if len(alt_parts) == 2:
                alt_text, width = alt_parts
        return (filename, alt_text, width)

    def raw_text(self):
        return self.alt_text

    def __str__(self) -> str:
        return "IMG[" + self.filename + "]"

