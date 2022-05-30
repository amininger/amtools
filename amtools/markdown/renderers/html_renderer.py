import re 
import os

from amtools.markdown.elements import *
from .html_templates import HtmlTemplates

NL_PLACEHOLDER = '_#!_NL_!#_'

class HtmlRenderer:
    def __init__(self, cur_dir=""):
        self.cur_dir = cur_dir
        self.renderers = { }
        self.renderers[HorizontalRule] = self.render_horizontal_rule
        self.renderers[Heading]        = self.render_heading
        self.renderers[TaskList]       = self.render_task_list
        self.renderers[BulletedList]   = self.render_bulleted_list
        self.renderers[NumberedList]   = self.render_numbered_list
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

    def render_bulleted_list(self, b_list: BulletedList) -> str:
        list_items = '\n'.join(self.render_list_item(li) for li in b_list.items)
        return HtmlTemplates.unordered_list(list_items) 

    def render_numbered_list(self, n_list: NumberedList) -> str:
        list_items = '\n'.join(self.render_list_item(li) for li in n_list.items)
        return HtmlTemplates.ordered_list(list_items) 

    def render_list_item(self, li: str) -> str:
        rendered_text = self.render_text_element(li)
        return HtmlTemplates.list_item(rendered_text)

    def render_task_list(self, t_list: TaskList) -> str:
        list_items = '\n'.join(self.render_task_list_item(li) for li in t_list.items)
        return HtmlTemplates.unordered_list(list_items, cls="contains-task-list")

    def render_task_list_item(self, li: TaskItem) -> str:
        item_text = self.render_text_element(li.text)
        return HtmlTemplates.task_list_item(item_text, li.symbol(), li.is_checked())
    
    def render_code_block(self, block: CodeBlock) -> str:
        compacted_block = block.text.replace('\n', NL_PLACEHOLDER)
        code_block = HtmlTemplates.code(compacted_block)
        return HtmlTemplates.pre(code_block)

    def render_block_quote(self, block: BlockQuote) -> str:
        rendered_text = "\n".join(self.render_text_element(line) for line in block.lines)
        return HtmlTemplates.blockquote(HtmlTemplates.p(rendered_text))

    def render_table(self, table: Table) -> str:
        headings = [ self.render_text_element(h) for h in table.headings ]
        rows = [ [ self.render_text_element(c) for c in row ] for row in table.rows ]
        return HtmlTemplates.table(headings, rows, table.widths)

    def render_paragraph(self, par: Paragraph) -> str:
        rendered_lines = [ self.render_text_element(el) for el in par.elements ]
        rendered_text = '\n<br>\n'.join(rendered_lines)
        return HtmlTemplates.p(rendered_text)

    def render_text_element(self, text) -> str:
        if isinstance(text, RawText):
            return text.raw_text()
        if isinstance(text, Tag):
            return self.render_tag(text)
        if isinstance(text, Hyperlink):
            return self.render_hyperlink(text)
        if isinstance(text, InlineText):
            rendered_children = " ".join(self.render_text_element(el) for el in text.elements)
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
            return rendered_children

        return str(text)

    def render_tag(self, tag: Tag) -> str:
        return HtmlTemplates.a("#" + tag.title, "", cls="tag red-tag")
    
    def render_hyperlink(self, link: Hyperlink) -> str:
        link_text = self.render_text_element(link.text)
        link_addr = link.addr
        if not link_addr.startswith("http") and not link_addr.startswith("www"):
            link_addr = os.path.join(self.cur_dir, link_addr)
        return HtmlTemplates.a(link_text, link_addr)




