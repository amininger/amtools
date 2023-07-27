import sys
import os

from amtools.filesystem import fsutil
from amtools.markdown.parsers import MarkdownParser
from amtools.markdown.renderers import HtmlRenderer, PdfRenderer

CSS_FILES = [ ]
if 'AMTOOLS_HOME' in os.environ:
    CSS_FILES.append( os.path.join(os.environ['AMTOOLS_HOME'], "res/pdf-theme.css" ))

def perror(text: str):
    print(text, file=sys.stderr)

def main():
    """ Converts one or more markdown files to html documents 
        --all: converts all markdown files in current dir """
    print_theme = False
    files = []
    for arg in sys.argv[1:]:
        if arg == "--all":
            files.extend([ f for f in os.listdir() if f.endswith(".md") ])
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
        ofile = ifile.replace(".md", ".html")
        with open(ifile, 'r') as f:
            markdown = f.read()
        markdown = fsutil.remove_metadata(markdown)
        make_html_doc_from_markdown(ofile, markdown, css_files)

def make_html_doc_from_markdown(filename, markdown, css_files):
    """ Renders the given markdown as an html document and saves it as the given file """
    elements = MarkdownParser.parse_string(markdown)
    renderer = HtmlRenderer()
    html = renderer.render_document(filename, elements, css_files=css_files)
    save_html_document(filename, html)

def save_html_document(filename:str, html:str):
    """ Writes the given html to a file """
    with open(filename, 'w') as f:
        f.write(html)

if __name__ == "__main__":
    main()
