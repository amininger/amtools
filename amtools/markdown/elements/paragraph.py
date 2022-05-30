from .markdown_element import MarkdownElement
from .inline_text import InlineText, LineBreak

class Paragraph(MarkdownElement):
    """ An entire paragraph of text (all text is wrapped in paragraphs) """

    def __init__(self, text: str):
        self.lines = [""]
        self.add_text(text)

        self.elements = []

    def add_text(self, text: str) -> None:
        text = text.strip()
        newline = False
        if text[-1] == '\\':
            newline = True
            text = text[:-1]

        self.lines[-1] = self.lines[-1] + " " + text
        if newline:
            self.lines.append("")

    def add_empty_line(self) -> None:
        if self.lines[-1] != "":
            self.lines.append("")

    def set_elements(self, elements: list) -> None:
        self.elements = elements
    
    def __str__(self) -> str:
        return "P(\n  " + '\n  '.join(el.raw_text() for el in self.elements) + "\n)"
        #return "P(\n  " + '\n  '.join(map(str, self.elements)) + "\n)"

