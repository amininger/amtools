
from .html_renderer import HtmlRenderer
from .menu_renderer import MenuRenderer

def make_renderer(name: str) -> HtmlRenderer:
    """ Returns an instance of the appropriate HtmlRenderer from its name
        menu - MenuRenderer
        default - HtmlRenderer
    """
    if name is not None:
        if name == "menu":
            return MenuRenderer()

    return HtmlRenderer()
