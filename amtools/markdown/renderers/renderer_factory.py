
from amtools.filesystem import FileContext

from .html_renderer import HtmlRenderer
from .menu_renderer import MenuRenderer

def create_renderer(name: str, url_mapper) -> HtmlRenderer:
    """ Returns an instance of the appropriate HtmlRenderer from its name
        menu - MenuRenderer
        pdf - PdfRenderer
        default - HtmlRenderer

        url_mapper is a function that maps absolute filesystem paths to a url
    """
    if name == "menu":
        return MenuRenderer(url_mapper)
    elif name == "pdf":
        return PdfRenderer(url_mapper)
    else:
        return HtmlRenderer(url_mapper)
