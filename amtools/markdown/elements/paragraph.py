
class Paragraph:
    """ An entire paragraph of text (all text is wrapped in paragraphs) """

    def __init__(self, text):
        self.text = text

    def add_line(self, line: str) -> None:
        self.text += '\n' + line
    
    def __str__(self) -> str:
        return "P(" + self.text + ")"

