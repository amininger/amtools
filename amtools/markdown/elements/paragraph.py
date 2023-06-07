from .markdown_element import MarkdownElement
from .inline_text import InlineText, LineBreak

class Paragraph(MarkdownElement):
    """ An entire paragraph of text (all text is wrapped in paragraphs) """

    def __init__(self, text: str):
        self.text = ""
        self.add_text(text)
        self.text_element = None

    def add_text(self, new_text: str) -> None:
        new_text = new_text.strip()
        newline = False

        if new_text[-1] == '\\':
            new_text = new_text[:-1]
            newline = True
        elif new_text.endswith('<br>'):
            new_text = new_text[:-4]
            newline = True

        self.text += ("\n" if self.text else "") + new_text + ("\n<br>" if newline else "")

    def __str__(self) -> str:
        return "P(\n  " + self.text_element.raw_text() + "\n)"
        #return "P(\n  " + '\n  '.join(map(str, self.elements)) + "\n)"

