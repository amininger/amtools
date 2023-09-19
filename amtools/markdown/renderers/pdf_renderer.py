import os
import sys
import random
import string
import subprocess
from tempfile import NamedTemporaryFile

from amtools.markdown.elements import *
from .html_templates import HtmlTemplates
from .html_renderer import HtmlRenderer

import numpy as np
from PIL import Image

def crop_image(file_name:str) -> str:
    """ Takes the given image file, crops to a tight box around the content,
        ignoring any transparent pixels
        Returns the saved cropped image name """
    # Read input image, and convert to NumPy array.
    img = np.array(Image.open(file_name))  

    # Find indices of non-white pixels
    idx = np.where(img[:, :, 0] < 250)

    # Get minimum and maximum index in both axes (top left corner and bottom right corner)
    x0, y0, x1, y1 = idx[1].min(), idx[0].min(), idx[1].max(), idx[0].max()

    # Add a little padding on the sides (to separate from adjacent text)
    H_PADDING = 18
    x0 = max(0, x0 - H_PADDING)
    x1 = min(len(img[0]), x1 + H_PADDING)
     
    # Add vertical padding if too small
    MIN_HEIGHT = 36
    height = y1 - y0
    if height < MIN_HEIGHT:
        y0 = max(0, y0 - (MIN_HEIGHT - height))
    y0 = max(0, y0 - 9) # More padding to top

    # Crop rectangle and convert to Image
    out = Image.fromarray(img[y0:y1+1, x0:x1+1, :])

    # Save the result (RGBA color format).
    out_file = NamedTemporaryFile(suffix='.png', delete = False)
    out.save(out_file.name)

    return out_file.name, (x1-x0, y1-y0)


def collect_latex_statements(elements: list):
    latex_statements = []
    for el in elements:
        if el == elements:
            continue
        if isinstance(el, LatexMath):
            latex_statements.append(el)
        latex_statements.extend(collect_latex_statements(el))
    return latex_statements

def render_latex_statements(latex_statements: list):
    with NamedTemporaryFile(mode='w', suffix='.md', delete=False) as f:
        f.write("<style> section { font-size: 36px; } </style>\n\n")
        f.write("\n\n---\n\n".join(map(str, latex_statements)))

    res = subprocess.run(['marp', '--images=png', f.name])
    if res.returncode != 0:
        print("create_marp_slides: Marp Error!: \n" + res.stderr)
        return

    for i, latex in enumerate(latex_statements):
        latex.rendered_image = f.name.replace(".md", f".{i+1:03}.png")


class PdfRenderer(HtmlRenderer):
    def __init__(self, url_mapper = None):
        super().__init__(url_mapper)

    def render_markdown_elements(self, elements: list) -> str:
        latex_statements = collect_latex_statements(elements)
        if len(latex_statements) > 0:
            render_latex_statements(latex_statements)
        return super().render_markdown_elements(elements)

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

    def render_text_element(self, text) -> str:
        if isinstance(text, LatexMath):
            return self.render_latex_math(text)
        return super().render_text_element(text)

    def render_latex_math(self, text: LatexMath) -> str:
        if text.rendered_image == None:
            return HtmlTemplates.code(str(text))
        cropped_img, dims = crop_image(text.rendered_image)
        return HtmlTemplates.img(cropped_img, text.raw_text(), cls="inline", width=int(dims[0]/3), height=(dims[1]/3))

    def render_callout(self, callout: Callout) -> str:
        rendered_title = self.render_text_element(callout.title)
        rendered_text = HtmlTemplates.bold(rendered_title) + "<br>"
        rendered_text += "\n".join(self.render_element(elem) for elem in callout.elements)
        return HtmlTemplates.blockquote(rendered_text)
    
    def render_image(self, img: Image) -> str:
        img_url = img.filename
        if self.is_relative(img_url):
            img_url = self.url_mapper(img_url)
        if img.width is not None:
            img_width = img.get_css_width()
            return HtmlTemplates.img(img_url, img.alt_text, style=f"width: {img_width};")
        else:
            return HtmlTemplates.img(img_url, img.alt_text)


