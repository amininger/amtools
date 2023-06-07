import sys

from amtools import FileReader
from amtools.filesystem import FileContext
from amtools.markdown.parsers import MarkdownParser
from amtools.markdown.renderers import HtmlRenderer

filename = "test-file.md"
if len(sys.argv) > 0:
    filename = sys.argv[1]

reader = FileReader(filename)
parser = MarkdownParser()
elements = parser.parse_markdown(reader)
print('\n'.join(str(el) for el in elements))

renderer = HtmlRenderer(FileContext())
html = renderer.render_markdown_elements(elements)
print(html)

