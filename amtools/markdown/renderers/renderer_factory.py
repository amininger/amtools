
from amtools.filesystem import FileContext

from .html_renderer import HtmlRenderer
from .menu_renderer import MenuRenderer

def create_renderer(name: str, context: FileContext) -> HtmlRenderer:
    """ Returns an instance of the appropriate HtmlRenderer from its name
        menu - MenuRenderer
        default - HtmlRenderer
    """
    if name is not None:
        if name == "menu":
            return MenuRenderer(context)

    return HtmlRenderer(context)
