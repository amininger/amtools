
from amtools import FileReader
from amtools.markdown.parsers import MarkdownParser
from amtools.markdown.renderers import HtmlRenderer

reader = FileReader("test-file.md")
parser = MarkdownParser()
elements = parser.parse_markdown(reader)
print('\n'.join(str(el) for el in elements))

renderer = HtmlRenderer()
html = renderer.render_markdown_elements(elements)
print(html)

