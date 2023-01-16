import re

from .markdown_element import MarkdownElement

class LineBreak:
    def __str__(self) -> str:
        return "[BR]"

class InlineText(MarkdownElement):
    def __init__(self, *elements):
        self.elements = []
        for el in elements:
            if isinstance(el, str) and len(el) > 0:
                self.elements.append(RawText(el))
            elif type(el) == RawText and len(el.text) > 0:
                self.elements.append(el)
            elif type(el) == InlineText:
                self.elements.extend(el.elements)
            else:
                self.elements.append(el)

    def raw_text(self) -> str:
        child_text = (el.raw_text().strip() for el in self.elements)
        return " ".join(t for t in child_text if len(t) > 0)

    def __str__(self) -> str:
        return "[T:" + " ".join(map(str, self.elements)) + "]"

class RawText(MarkdownElement):
    def __init__(self, text: str):
        self.text = text

    def raw_text(self) -> str:
        return self.text
        
    def __str__(self) -> str:
        return "\"" + self.text + "\""

class Tag(InlineText):
    def __init__(self, title: str):
        self.title = title

    def raw_text(self) -> str:
        return self.title

    def __str__(self) -> str:
        return "[#" + self.title + "]"

class BoldItalicsText(InlineText):
    def __str__(self) -> str:
        return "[B+I:" + " ".join(map(str, self.elements)) + "]"

class BoldText(InlineText):
    def __str__(self) -> str:
        return "[B:" + " ".join(map(str, self.elements)) + "]"

class ItalicsText(InlineText):
    def __str__(self) -> str:
        return "[I:" + " ".join(map(str, self.elements)) + "]"

class CodeText(InlineText):
    def __str__(self) -> str:
        return "[C:" + " ".join(map(str, self.elements)) + "]"

class LatexText(InlineText):
    def __str__(self) -> str:
        return "[$:" + " ".join(map(str, self.elements)) + "]"

class StrikethroughText(InlineText):
    def __str__(self) -> str:
        return "[--" + " ".join(map(str, self.elements)) + "--]"

class HighlightText(InlineText):
    def __str__(self) -> str:
        return "[H:" + " ".join(map(str, self.elements)) + "]"


    

