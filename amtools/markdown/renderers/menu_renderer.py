import os

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

    def __init__(self, cur_dir=""):
        super().__init__(cur_dir)
        self.logo = ''
        self.title = ''
        self.content = []

    def render_markdown_elements(self, elements: list):
        for el in elements:
            self.content.append(self.render_element(el))

        return render_menu(self.logo, self.title, '\n'.join(self.content))

    def render_heading(self, heading: Heading):
        if heading.weight == 1:
            rendered_title = self.render_text_element(heading.title)
            self.title = f"""<h1 id="menu-title"><a href="{self.cur_dir}">{rendered_title}</a></h1>"""
            return ""

        return super().render_heading(heading)

    def render_bulleted_list(self, b_list: BulletedList):
        btns = []
        for item in b_list.items:
            for el in item.elements:
                if isinstance(el, Hyperlink):
                    btn_text = self.render_text_element(el.text)
                    btns.append(self.render_menu_button(btn_text, el.addr))

        return '\n'.join(btns)
    
    def render_menu_button(self, btn_text: str, btn_link: str):
        full_link = os.path.join(self.cur_dir, btn_link)
        return f"""<a href="{full_link}"><button class="menu-btn">{btn_text}</button></a>"""

