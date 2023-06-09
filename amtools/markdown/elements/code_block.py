from .markdown_element import MarkdownElement

class CodeBlock(MarkdownElement):
    """ A block of verbatim code text """

    def __init__(self, text: str, lang:str):
        self.text = text
        self.lang = lang.strip()
    
    def __str__(self) -> str:
        return "######### CODE BLOCK ##########\n" + self.text + '\n##########################'
