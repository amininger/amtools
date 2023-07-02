import sys
import os
from tempfile import mkstemp

from io import BytesIO
from xhtml2pdf import pisa

from amtools.filesystem import fsutil
from amtools.markdown.parsers import MarkdownParser
from amtools.markdown.renderers import PdfRenderer

def perror(text: str):
    print(text, file=sys.stderr)

def main():
    """ Converts one or more markdown files to pdf documents 
        --all: converts all markdown files in current dir
        --print: uses a printer-friendly theme without much color """
    print_theme = False
    files = []
    for arg in sys.argv[1:]:
        if arg == "--all":
            files.extend([ f for f in os.listdir() if f.endswith(".md") ])
        elif arg == "--print":
            print_theme = True
        else:
            files.append(arg)

    if len(files) == 0:
        perror("Requires 1 or more files to convert")
        perror("or --all to convert all md in the cur dir")
        sys.exit(0)

    css_files = [ ]
    if 'AMTOOLS_HOME' not in os.environ:
        perror("Error: Add $AMTOOLS_HOME to environment for CSS themes")
        sys.exit(0)
    elif print_theme:
        css_files.append( os.path.join(os.environ['AMTOOLS_HOME'], "res/print-pdf-theme.css" ))
    else:
        css_files.append( os.path.join(os.environ['AMTOOLS_HOME'], "res/pdf-theme.css" ))

    # Render each file
    for ifile in files:
        ofile = ifile.replace(".md", ".pdf")
        with open(ifile, 'r') as f:
            markdown = f.read()
        markdown = fsutil.remove_metadata(markdown)
        make_pdf_from_markdown(ofile, markdown, css_files)

def make_pdf_from_markdown(filename, markdown, css_files):
    """ Renders the given markdown as a pdf document and saves it as the given file """
    elements = MarkdownParser.parse_string(markdown)
    renderer = PdfRenderer()
    pdf_html = renderer.render_document(filename, elements, css_files=css_files)
    #print(pdf_html)
    save_pdf_document(filename, pdf_html)

def save_pdf_document(filename:str, pdf_html:str):
    """ Writes the given html to a pdf file using xhtml2pdf """
    # write html to a temporary file
    # can used NamedTemporaryFile if using python 2.6+
    fid, temp_file = mkstemp(dir='/tmp')
    f = open(temp_file, 'w')
    f.write(pdf_html)
    f.close()

    # now create pdf from the html
    cmd = f"xhtml2pdf {temp_file} {filename}"
    os.system(cmd)
    os.remove(temp_file)

if __name__ == "__main__":
    main()
