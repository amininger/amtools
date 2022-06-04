import os

from amtools.filesystem import FileContext
from amtools.markdown.elements import *
from .html_templates import HtmlTemplates
from .html_renderer import HtmlRenderer

class PdfRenderer(HtmlRenderer):
    def __init__(self, context: FileContext):
        super().__init__(context)

    def render_table(self, table: Table) -> str:
        headings = [ self.render_text_element(h) for h in table.headings ]
        rows = [ [ self.render_text_element(c) for c in row ] for row in table.rows ]
        wid_total = sum(table.widths)
        widths = [ "width: " + str((w*100)//wid_total) + "%;" for w in table.widths ]
        return HtmlTemplates.table(headings, rows, widths)
    
    def render_hyperlink(self, link: Hyperlink) -> str:
        link_text = self.render_text_element(link.text)
        if link_addr.startswith("http") or link_addr.startswith("www"):
            return HtmlTemplates.a(link_text, link_addr)
        return link_text
    
    def render_image(self, img: Image) -> str:
        img_url = img.filename
        if not img.filename.startswith("http") and not img.filename.startswith("www") and not img.filename.startswith("/"):
            img_url = self.context.get_local(img.filename)
        if img.width is not None:
            img_width = img.width if '%' in img.width else img.width + "px"
            return HtmlTemplates.img(img_url, img.alt_text, style=f"width: {img_width};")
        else:
            return HtmlTemplates.img(img_url, img.alt_text)




