import sys
import os

from .markdown_tools import make_pdf_from_markdown

if __name__ == "__main__":
    if len(sys.argv) == 1:
        print("Requires 1 or more files to convert")
        print("or --all to convert all in the cur dir")
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
