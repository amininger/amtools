
from amtools.markdown.elements import *

from .html_renderer import HtmlRenderer
from .html_templates import HtmlTemplates

def render_menu(logo, title, content):
    return f"""
    <img id="show-menu-icon" class="top-menu-only" src="/static/icons/menu-light.png" alt="Show Menu">
    <div class="image side-menu-only">
        {logo}
    </div>
    {title}
    <div id="menu-content" label="Menu Links">
        {content}
    </div>
    """

class MenuRenderer(HtmlRenderer):

    def __init__(self):
        self.logo = ''
        self.title = ''
        self.content = []

    def render_markdown_elements(self, elements: list):
        for el in elements:
            self.content.append(self.render_element(el))

        return render_menu(self.logo, self.title, '\n'.join(self.content))

    def render_heading(self, heading: Heading):
        if heading.weight == 1:
            rendered_title = self.render_inline_text(heading.title)
            self.title = f"""<h1 id="menu-title"><a href="../">{rendered_title}</a></h1>"""
            return ""

        return super().render_heading(heading)

    def render_bulleted_list(self, b_list: BulletedList):
        btns = []
        for btn_info in b_list.items:
            btn_info = btn_info.strip()
            close_br = btn_info.index(']')
            if close_br == -1:
                btn_text = btn_info
                btn_addr = ""
            else:
                btn_text = btn_info[1:close_br]
                btn_addr = btn_info[close_br+2:-1]
            btns.append(self.render_menu_button(btn_text, btn_addr))

        return '\n'.join(btns)
    
    def render_menu_button(self, btn_text: str, btn_link: str):
        return f"""<a href="{btn_link}"><button class="menu-btn">{btn_text}</button></a>"""

