from .markdown_element import MarkdownElement

class CodeBlock(MarkdownElement):
    """ A block of verbatim code text """

    def __init__(self, text: str):
        self.text = text
    
    def __str__(self) -> str:
        return "######### CODE BLOCK ##########\n" + self.text + '\n##########################'
