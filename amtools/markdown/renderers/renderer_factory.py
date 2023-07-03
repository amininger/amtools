
from amtools.filesystem import FileContext

from .html_renderer import HtmlRenderer
from .menu_renderer import MenuRenderer

def create_renderer(name: str, context: FileContext) -> HtmlRenderer:
    """ Returns an instance of the appropriate HtmlRenderer from its name
        menu - MenuRenderer
        pdf - PdfRenderer
        default - HtmlRenderer
    """
    if name == "menu":
        return MenuRenderer(context)
    elif name == "pdf":
        return PdfRenderer(context)
    else:
        return HtmlRenderer(context)
