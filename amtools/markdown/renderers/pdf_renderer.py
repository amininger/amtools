import os
import sys

from amtools.filesystem import FileContext
from amtools.markdown.elements import *
from .html_templates import HtmlTemplates
from .html_renderer import HtmlRenderer

def pdf_doc_template(title, css_html, body_html):
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title}</title>
    {css_html}
</head>
<body>
<div class="content">
{body_html}
</div>
</body>
</html>
"""

class PdfRenderer(HtmlRenderer):
    def __init__(self, css_files:list = [], context: FileContext = FileContext.DEFAULT):
        super().__init__(context)
        self.css_files = css_files

    def render_table(self, table: Table) -> str:
        headings = [ self.render_text_element(h) for h in table.headings ]
        rows = [ [ self.render_text_element(c) for c in row ] for row in table.rows ]
        wid_total = sum(table.widths)
        widths = [ "width: " + str((w*100)//wid_total) + "%;" for w in table.widths ]
        return HtmlTemplates.table(headings, rows, widths)
    
    def render_hyperlink(self, link: Hyperlink) -> str:
        link_text = self.render_text_element(link.text)
        if not self.is_relative(link.addr):
            return HtmlTemplates.a(link_text, link.addr)
        return link_text
    
    def render_image(self, img: Image) -> str:
        img_url = img.filename
        if self.is_relative(img_url):
            img_url = self.context.get_local(img_url)
        if img.width is not None:
            img_width = img.width if '%' in img.width else img.width + "px"
            return HtmlTemplates.img(img_url, img.alt_text, style=f"width: {img_width};")
        else:
            return HtmlTemplates.img(img_url, img.alt_text)

    def render_document(self, title:str, elements:list):
        html = self.render_markdown_elements(elements)
        css_html = self.render_inline_css()
        return pdf_doc_template(title, css_html, html)

    def render_inline_css(self):
        css_html = []
        for css_file in self.css_files:
            if not os.path.exists(css_file):
                print(f"CSS File {css_file} does not exist", file=sys.stderr)
                continue
            with open(css_file, 'r') as f:
                css_text = f.read()
                css_html.append(f"<style>\n{css_text}\n</style>")
        return "\n".join(css_html)

