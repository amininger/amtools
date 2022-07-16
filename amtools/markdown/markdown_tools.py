import os
from io import BytesIO
from xhtml2pdf import pisa

from amtools.filesystem import MarkdownDoc, FileContext
from amtools.markdown.parsers import MarkdownParser
from amtools.markdown.renderers import PdfRenderer

CSS_FILES = [ ]
if 'AMTOOLS_HOME' in os.environ:
    CSS_FILES.append( os.path.join(os.environ['AMTOOLS_HOME'], "pdf-theme.css" ))
print("CSS_FILES", CSS_FILES)

def make_pdf_from_markdown(filename, markdown):
    context = FileContext("", "", "")
    elements = MarkdownParser.parse_string(markdown)
    renderer = PdfRenderer(context)
    html = renderer.render_markdown_elements(elements)
    pdf_html = make_pdf_html(filename, html, CSS_FILES)

    result = BytesIO()
    pdf = pisa.pisaDocument(BytesIO(pdf_html.encode("ISO-8859-1")), result)
    if not pdf.err:
        with open(filename, 'wb') as f:
            f.write(result.getvalue())
    return None

def make_pdf_html(title, body_html, css_files=[]):
    css_html = []
    for css_file in css_files:
        if not os.path.exists(css_file):
            continue
        with open(css_file, 'r') as f:
            css_text = f.read()
        css_html.append(f"<style>\n{css_text}\n</style>")
    inline_css = "\n".join(css_html)
    return f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title}</title>
    {inline_css}
</head>
<body>
<div class="content">
{body_html}
</div>
</body>
</html>
"""

