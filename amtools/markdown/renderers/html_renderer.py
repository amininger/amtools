import re 
import os

from amtools.markdown.elements import *
from .html_templates import HtmlTemplates

NL_PLACEHOLDER = '_#!_NL_!#_'

class HtmlRenderer:
    def __init__(self, cur_dir=""):
        self.cur_dir = cur_dir

    def render_markdown_elements(self, elements: list) -> str:
        """ Renders a list of markdown elements into a string of html """
        body = '\n'.join(self.render_element(el) for el in elements)
        html = body.replace(NL_PLACEHOLDER, '\n')
        return html
    
    def render_element(self, elem) -> str:
        """ Renders a single markdown element as html and returns it """
        if isinstance(elem, HorizontalRule):
            return self.render_horizontal_rule(elem)
        elif isinstance(elem, Heading):
            return self.render_heading(elem)
        elif isinstance(elem, BulletedList):
            return self.render_bulleted_list(elem)
        elif isinstance(elem, NumberedList):
            return self.render_numbered_list(elem)
        elif isinstance(elem, CodeBlock):
            return self.render_code_block(elem)
        elif isinstance(elem, Paragraph):
            return self.render_paragraph(elem)
        elif isinstance(elem, InlineText):
            return self.render_text_element(elem)
                
        return str(elem)


    def render_horizontal_rule(self, hr: HorizontalRule) -> str:
        return HtmlTemplates.hr()

    def render_heading(self, heading: Heading) -> str:
        rendered_title = self.render_text_element(heading.title)
        return HtmlTemplates.heading(heading.weight, rendered_title) 

    def render_bulleted_list(self, b_list: BulletedList) -> str:
        list_items = '\n'.join(self.render_list_item(li) for li in b_list.items)
        return HtmlTemplates.unordered_list(list_items) 

    def render_numbered_list(self, n_list: NumberedList) -> str:
        list_items = '\n'.join(self.render_list_item(li) for li in n_list.items)
        return HtmlTemplates.ordered_list(list_items) 

    def render_list_item(self, li: str) -> str:
        rendered_text = self.render_text_element(li)
        return HtmlTemplates.list_item(rendered_text)
    
    def render_code_block(self, block: CodeBlock) -> str:
        compacted_block = block.text.replace('\n', NL_PLACEHOLDER)
        return HtmlTemplates.code(compacted_block)

    def render_paragraph(self, par: Paragraph) -> str:
        rendered_lines = [ self.render_text_element(el) for el in par.elements ]
        rendered_text = '\n<br>\n'.join(rendered_lines)
        return HtmlTemplates.p(rendered_text)

    def render_text_element(self, text: str) -> str:
        if isinstance(text, RawText):
            return text.raw_text()
        if isinstance(text, Hyperlink):
            return self.render_hyperlink(text)
        if isinstance(text, InlineText):
            rendered_children = "".join(self.render_text_element(el) for el in text.elements)
            if isinstance(text, BoldText):
                return HtmlTemplates.bold(rendered_children)
            if isinstance(text, ItalicsText):
                return HtmlTemplates.italics(rendered_children)
            if isinstance(text, CodeText):
                return HtmlTemplates.inline_code(rendered_children)
            return rendered_children

        return str(text)
    
    def render_hyperlink(self, link: Hyperlink) -> str:
        link_addr = os.path.join(self.cur_dir, link.addr)
        return HtmlTemplates.a(link.text, link_addr)




