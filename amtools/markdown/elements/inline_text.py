import re

class LineBreak:
    def __str__(self) -> str:
        return "[BR]"

class InlineText:
    def __init__(self, *elements):
        self.elements = []
        for el in elements:
            if isinstance(el, str):
                if len(el.strip()) > 0:
                    self.elements.append(RawText(el))
            elif type(el) == RawText:
                if len(el.text.strip()) > 0:
                    self.elements.append(el)
            elif type(el) == InlineText:
                self.elements.extend(el.elements)
            else:
                self.elements.append(el)

    def __str__(self) -> str:
        return "[T:" + " ".join(map(str, self.elements)) + "]"

class RawText:
    def __init__(self, text: str):
        self.text = text
        
    def __str__(self) -> str:
        return self.text

class BoldText(InlineText):
    def __str__(self) -> str:
        return "[B:" + " ".join(map(str, self.elements)) + "]"

class ItalicsText(InlineText):
    def __str__(self) -> str:
        return "[I:" + " ".join(map(str, self.elements)) + "]"

class CodeText(InlineText):
    def __str__(self) -> str:
        return "[C:" + " ".join(map(str, self.elements)) + "]"

    
