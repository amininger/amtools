from .markdown_element import MarkdownElement
from .blockquote import BlockQuote

def make_custom_block(block_type: str, elements, *args):
    args = [ arg.strip() for arg in args if len(arg.strip()) > 0]
    if block_type == "card":
        return Card(args[0], elements)
    elif block_type == "link_list":
        return LinkList(elements)

    return BlockQuote(elements)

class Card(MarkdownElement):
    
    def __init__(self, title, elements):
        self.title = title
        self.elements = elements

    def __str__(self):
        return f"Card[{self.title}]\n" + "\n".join(map(str, self.elements)) + "--------------\n"

class LinkList(MarkdownElement):
    """ A list of navigation links """

    def __init__(self, elements):
        self.elements = elements
    
    def __str__(self) -> str:
        return "| " + "\n| ".join(str(elem) for elem in self.elements)

