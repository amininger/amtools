
from .markdown_element import MarkdownElement

class BlockQuote(MarkdownElement):
    """ A quoted block of text """

    def __init__(self):
        self.text = ""

    def add_line(self, line: str) -> None:
        self.text += " " + line
    
    def __str__(self) -> str:
        words = self.text.split(" ")
        text = "| " + "\n| ".join(" ".join(words[i:i+10]) for i in range(0, len(words), 10))
        return text
