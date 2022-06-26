import sys

from .markdown_tools import make_pdf_from_markdown

if __name__ == "__main__":
    if len(sys.argv) == 1:
        print("Arg 1: Name of the markdown file")
        print("Arg 2: Optional - Name of the output pdf file")
        sys.exit(0)

    ifile = sys.argv[1]
    if len(sys.argv) > 2:
        ofile = sys.argv[2]
    else:
        ofile = ifile.replace(".md", ".pdf")

    with open(ifile, 'r') as f:
        markdown = f.read()

    make_pdf_from_markdown(ofile, markdown)
