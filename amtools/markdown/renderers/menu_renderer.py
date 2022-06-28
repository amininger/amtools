import os

from amtools.filesystem import FileContext
from amtools.markdown.elements import *

from .html_renderer import HtmlRenderer
from .html_templates import HtmlTemplates

def render_menu(logo, title, content):
    return f"""
    <img id="show-menu-icon" class="top-menu-only" src="/static/img/icons/menu-light.png" alt="Show Menu">
    <a href="/">
    <div class="image side-menu-only">
        {logo}
    </div>
    </a>
    {title}
    <div id="menu-content" label="Menu Links">
        {content}
    </div>
    """

class MenuRenderer(HtmlRenderer):

    def __init__(self, context: FileContext, menu_header="", menu_footer=""):
        super().__init__(context)
        self.logo = ''
        self.title = ''
        self.content = []
        self.header = menu_header
        self.footer = menu_footer

    def render_markdown_elements(self, elements: list):
        for el in elements:
            self.content.append(self.render_element(el))

        content = self.header + '\n' + '\n'.join(self.content) + '\n' + self.footer
        return render_menu(self.logo, self.title, content)

    def render_heading(self, heading: Heading):
        if heading.weight == 1:
            rendered_title = self.render_text_element(heading.title)
            self.title = HtmlTemplates.heading(1, rendered_title, id='menu-title')
            return ""

        return super().render_heading(heading)

    def render_image(self, img: Image) -> str:
        img_url = img.filename
        if self.is_relative(img_url):
            img_url = self.context.get_media_url(img_url)
        self.logo = HtmlTemplates.img(img_url, img.alt_text)
        return ""

    def render_bulleted_list(self, b_list: BulletedList):
        btns = []
        for item in b_list.items:
            for el in item.elements:
                if isinstance(el, Hyperlink):
                    btn_text = self.render_text_element(el.text)
                    btns.append(self.render_menu_button(btn_text, el.addr))

        return '\n'.join(btns)
    
    def render_menu_button(self, btn_text: str, btn_link: str):
        full_link = self.context.get_url(btn_link)
        return f"""<a href="{full_link}"><button class="menu-btn">{btn_text}</button></a>"""

