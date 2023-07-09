import os
import sys
import random
import string
from tempfile import mkstemp

from amtools.markdown.elements import *
from .html_templates import HtmlTemplates
from .html_renderer import HtmlRenderer

import matplotlib.pyplot as plt
import numpy as np
from PIL import Image

def render_math_expression(math_expr: str) -> str:
    """ Takes the given latex math expression,
        renders it to a png file using latex
        and saves it in /tmp, 
        returns the filename """

    # Creates a random filename in /tmp
    file_name = ''.join(random.choice(string.ascii_lowercase) for i in range(12))
    file_name = f"/tmp/math_{file_name}.png"

    # Set the LaTeX font
    plt.rcParams['text.usetex'] = True
    plt.rcParams['text.latex.preamble'] = r'\usepackage{amsmath}'

    # Add $ symbols to format the string as an inline math expression
    inline_expr = f"\\boldmath${math_expr}$"

    # Create a plot with the expression
    fig, ax = plt.subplots(figsize=(20, 5))
    ax.text(0.5, 0.5, inline_expr, size=20, ha='center', weight="bold")

    # Remove the plot axes
    ax.set_axis_off()

    # Save the plot as a PNG with a transparent background
    plt.savefig(fname=file_name, format="png", transparent=True, bbox_inches='tight', pad_inches=0.0, dpi=200)
    plt.close(fig)

    return file_name

def crop_image(file_name:str) -> str:
    """ Takes the given image file, crops to a tight box around the content,
        ignoring any transparent pixels
        Returns the saved cropped image name """
    # Read input image, and convert to NumPy array.
    img = np.array(Image.open(file_name))  # img is 1080 rows by 1920 cols and 4 color channels, the 4'th channel is alpha.

    # Find indices of non-transparent pixels (indices where alpha channel value is above zero).
    idx = np.where(img[:, :, 3] > 0)

    # Get minimum and maximum index in both axes (top left corner and bottom right corner)
    x0, y0, x1, y1 = idx[1].min(), idx[0].min(), idx[1].max(), idx[0].max()

    # Add a little padding on the sides (to separate from adjacent text)
    x0 = max(0, x0-25)
    x1 = min(len(img[0]), x1+25)

    # Crop rectangle and convert to Image
    out = Image.fromarray(img[y0:y1+1, x0:x1+1, :])

    # Save the result (RGBA color format).
    out_file = file_name.split('.')[0] + "_cr.png"
    out.save(out_file)

    return out_file, (x1-x0, y1-y0)

class PdfRenderer(HtmlRenderer):
    def __init__(self, url_mapper = None):
        super().__init__(url_mapper)

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
        if isinstance(text, LatexText):
            return self.render_latex_math(text)
        return super().render_text_element(text)

    def render_latex_math(self, text: LatexText) -> str:
        temp_img = render_math_expression(text.raw_text())
        cropped_img, dims = crop_image(temp_img)
        #print("Rendered Math Expression: " + text.raw_text())
        return HtmlTemplates.img(cropped_img, text.raw_text(), cls="inline", width=int(dims[0]/4), height=(dims[1]/4))

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


