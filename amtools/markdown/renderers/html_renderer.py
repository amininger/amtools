import re 
import os

from amtools.filesystem import FileContext
from amtools.markdown.elements import *
from .html_templates import HtmlTemplates

NL_PLACEHOLDER = '_#!_NL_!#_'


class HtmlRenderer:
    def __init__(self, context: FileContext):
        self.context = context
        self.renderers = { }
        self.renderers[HorizontalRule] = self.render_horizontal_rule
        self.renderers[Heading]        = self.render_heading
        self.renderers[Image]          = self.render_image
        self.renderers[TaskList]       = self.render_task_list
        self.renderers[ListBlock]      = self.render_list_block
        self.renderers[ListItem]       = self.render_list_item
        self.renderers[CodeBlock]      = self.render_code_block
        self.renderers[BlockQuote]     = self.render_block_quote
        self.renderers[Table]          = self.render_table
        self.renderers[Paragraph]      = self.render_paragraph
        self.renderers[InlineText]     = self.render_text_element

    def render_markdown_elements(self, elements: list) -> str:
        """ Renders a list of markdown elements into a string of html """
        body = '\n'.join(self.render_element(el) for el in elements)
        html = body.replace(NL_PLACEHOLDER, '\n')
        return html
    
    def render_element(self, elem) -> str:
        """ Renders a single markdown element as html and returns it """
        if type(elem) in self.renderers:
            return self.renderers[type(elem)](elem)
        else:
            print("HtmlRenderer.render_element: unknown element type " + str(type(elem)))
            return str(elem)

    def render_horizontal_rule(self, hr: HorizontalRule) -> str:
        return HtmlTemplates.hr()

    def render_heading(self, heading: Heading) -> str:
        rendered_title = self.render_text_element(heading.title)
        return HtmlTemplates.heading(heading.weight, rendered_title) 

    def render_list_block(self, list_block: ListBlock) -> str:
        list_elems = '\n'.join(self.render_element(elem) for elem in list_block.elements)
        if list_block.list_type == ListType.ORDERED:
            return HtmlTemplates.ordered_list(list_elems) 
        else:
            return HtmlTemplates.unordered_list(list_elems) 

    def render_list_item(self, li, **kwargs) -> str:
        rendered_text = self.render_text_element(li.text)
        return HtmlTemplates.list_item(rendered_text, **kwargs)

    def render_task_list(self, t_list: TaskList) -> str:
        list_items = '\n'.join(self.render_task_list_item(li) for li in t_list.items)
        return HtmlTemplates.unordered_list(list_items, cls="contains-task-list")

    def render_task_list_item(self, li: TaskItem) -> str:
        item_text = self.render_text_element(li.text)
        return HtmlTemplates.task_list_item(item_text, li.symbol(), li.is_checked())
    
    def render_code_block(self, block: CodeBlock) -> str:
        compacted_block = block.text.replace('\n', NL_PLACEHOLDER)
        if block.lang != "":
            code_block = HtmlTemplates.code(compacted_block, cls=('language-' + block.lang))
        else:
            code_block = HtmlTemplates.code(compacted_block)
        return HtmlTemplates.pre(code_block)

    def render_block_quote(self, block: BlockQuote) -> str:
        rendered_text = "\n".join(self.render_element(elem) for elem in block.elements)
        return HtmlTemplates.blockquote(rendered_text)

    def render_table(self, table: Table) -> str:
        headings = [ self.render_text_element(h) for h in table.headings ]
        rows = [ [ self.render_text_element(c) for c in row ] for row in table.rows ]
        widths = [ "flex: " + str(w) + ";" for w in table.widths ]
        return HtmlTemplates.table(headings, rows, widths)

    def render_paragraph(self, par: Paragraph) -> str:
        rendered_text = self.render_text_element(par.text_element)
        return HtmlTemplates.p(rendered_text)

    def render_text_element(self, text) -> str:
        if isinstance(text, RawText):
            return text.raw_text()
        if isinstance(text, Tag):
            return self.render_tag(text)
        if isinstance(text, Hyperlink):
            return self.render_hyperlink(text)
        if isinstance(text, InlineText):
            rendered_children = "".join(self.render_text_element(el) for el in text.elements)
            if isinstance(text, BoldText):
                return HtmlTemplates.bold(rendered_children)
            if isinstance(text, ItalicsText):
                return HtmlTemplates.italics(rendered_children)
            if isinstance(text, CodeText):
                return HtmlTemplates.code(rendered_children)
            if isinstance(text, StrikethroughText):
                return HtmlTemplates.delete(rendered_children)
            if isinstance(text, HighlightText):
                return HtmlTemplates.mark(rendered_children)
            if isinstance(text, Image):
                return self.render_image(text)
            return rendered_children

        return str(text)

    def render_tag(self, tag: Tag) -> str:
        return HtmlTemplates.a("#" + tag.title, "", cls="tag red-tag")

    def is_relative(self, addr):
        for pattern in [ 'http', 'www', '/', 'mailto' ]:
            if addr.startswith(pattern):
                return False
        return True
    
    def render_hyperlink(self, link: Hyperlink) -> str:
        link_text = self.render_text_element(link.text)
        link_addr = link.addr
        if self.is_relative(link_addr):
            link_addr = self.context.get_url(link_addr)
        if link.title is None:
            return HtmlTemplates.a(link_text, link_addr)
        else:
            return HtmlTemplates.a(link_text, link_addr, title=link.title)
    
    def render_image(self, img: Image) -> str:
        img_url = img.filename
        if self.is_relative(img_url):
            img_url = self.context.get_media_url(img_url)
        if img.width is not None:
            img_width = img.width if '%' in img.width else img.width + "px"
            return HtmlTemplates.img(img_url, img.alt_text, style=f"width: {img_width};")
        else:
            return HtmlTemplates.img(img_url, img.alt_text)




