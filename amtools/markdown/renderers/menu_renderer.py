import os

from amtools.filesystem import FileContext
from amtools.markdown.elements import *

from .html_renderer import HtmlRenderer
from .html_templates import HtmlTemplates

class MenuRenderer(HtmlRenderer):
    def __init__(self, url_mapper):
        super().__init__(url_mapper)

    def unroll_nested_lists(self, list_block: ListBlock, depth:int=0):
        list_items = []
        for elem in list_block.elements:
            if isinstance(elem, ListItem):
                list_items.append( (elem, depth) )
            elif isinstance(elem, ListBlock):
                list_items.extend(self.unroll_nested_lists(elem, depth+1))
        return list_items

    def render_list_block(self, list_block: ListBlock):
        btns = []
        list_items = self.unroll_nested_lists(list_block)
        for item in list_items:
            for el in item[0].text.elements:
                if isinstance(el, Hyperlink):
                    btn_text = self.render_text_element(el.text)
                    btns.append(self.render_menu_button(btn_text, el.addr, f"indent-{item[1]}"))

        return '\n'.join(btns)
    
    def render_menu_button(self, btn_text: str, btn_link: str, cls: str):
        full_link = self.url_mapper(btn_link)
        return f"""<a href="{full_link}" class="nav-btn {cls}">{btn_text}</a>"""

