import re

from .markdown_element import MarkdownElement

SPECIAL_ELEMENTS = {
    'pb': "<div class='pb'>&nbsp;</div>",
    'page-break': "<div class='pb'>&nbsp;</div>",
    'br:xs': "<div class='vs-xs'>&nbsp;</div>",
    'br:sm': "<div class='vs-sm'>&nbsp;</div>",
    'br:md': "<div class='vs-md'>&nbsp;</div>",
    'br:lg': "<div class='vs-lg'>&nbsp;</div>",
    'br:xl': "<div class='vs-xl'>&nbsp;</div>",
    'br:xxl': "<div class='vs-xxl'>&nbsp;</div>",
}

class HtmlComment(MarkdownElement):
    def __init__(self, comment_text: str):
        if comment_text.strip() in SPECIAL_ELEMENTS:
            self.comment = SPECIAL_ELEMENTS[comment_text.strip()]
        else:
            self.comment = f"<!-- {comment_text} -->"

    def __str__(self) -> str:
        return self.comment
