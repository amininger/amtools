from .markdown_element import MarkdownElement

class HorizontalRule(MarkdownElement):
    """ Represents a horizontal line in the file (--- or ===) """

    def __str__(self):
        return "-------------------------------------------------"

