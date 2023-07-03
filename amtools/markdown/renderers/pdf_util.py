import os
from io import BytesIO
from django.http import HttpResponse
from django.conf import settings

from xhtml2pdf import pisa

from amtools.filesystem import MarkdownDoc

from .html_util import HtmlUtil

class PdfUtil:

    def pdf_from_md(doc: MarkdownDoc):
        html = HtmlUtil.get_pdf_html(doc)
        html = PdfUtil.make_full_html_doc(doc.get_title(), html, css_files=["pdf-theme.css"])
        result = BytesIO()
        pdf = pisa.pisaDocument(BytesIO(html.encode("UTF-8")), result)
        if not pdf.err:
            return result.getvalue()
        return None

    def make_full_html_doc(title, body_html, css_files=[]):
        css_html = []
        for css_file in css_files:
            path = os.path.join(settings.BASE_DIR, 'fsa_home/static/css', css_file)
            if not os.path.exists(path):
                continue
            with open(path, 'r') as f:
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

