import sys
import os

from io import BytesIO
from xhtml2pdf import pisa

from amtools.markdown.parsers import MarkdownParser
from amtools.markdown.renderers import PdfRenderer

CSS_FILES = [ ]
if 'AMTOOLS_HOME' in os.environ:
    CSS_FILES.append( os.path.join(os.environ['AMTOOLS_HOME'], "res/pdf-theme.css" ))

def main():
    """ Converts one or more markdown files to pdf documents """
    if len(sys.argv) == 1:
        print("Requires 1 or more files to convert")
        print("or --all to convert all md in the cur dir")
        sys.exit(0)

    if sys.argv[1] == "--all":
        files = [ f for f in os.listdir() if f.endswith(".md") ]
    else:
        files = sys.argv[1:]

    for ifile in files:
        ofile = ifile.replace(".md", ".pdf")
        with open(ifile, 'r') as f:
            markdown = f.read()
        make_pdf_from_markdown(ofile, markdown)

def make_pdf_from_markdown(filename, markdown):
    """ Renders the given markdown as a pdf document and saves it as the given file """
    elements = MarkdownParser.parse_string(markdown)
    renderer = PdfRenderer(CSS_FILES)
    pdf_html = renderer.render_document(filename, elements)
    print(pdf_html)
    save_pdf_document(filename, pdf_html)

def save_pdf_document(filename:str, pdf_html:str):
    """ Writes the given html to a pdf file using xhtml2pdf """
    result = BytesIO()
    pdf = pisa.pisaDocument(BytesIO(pdf_html.encode("UTF-8")), result)
    if pdf.err:
        print("PDF ERROR:", pdf.err)
        return
    with open(filename, 'wb') as f:
        f.write(result.getvalue())

if __name__ == "__main__":
    main()
