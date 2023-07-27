import re 
import os

from amtools.markdown.elements import *
from .html_templates import HtmlTemplates

NL_PLACEHOLDER = '_#!_NL_!#_'

DEFAULT_URL_MAPPER = lambda s: s

class HtmlRenderer:
    def __init__(self, url_mapper = None):
        self.url_mapper = DEFAULT_URL_MAPPER if url_mapper is None else url_mapper
        self.renderers = { }
        self.renderers[HorizontalRule] = self.render_horizontal_rule
        self.renderers[Heading]        = self.render_heading
        self.renderers[Image]          = self.render_image
        self.renderers[LinkedImage]    = self.render_linked_image
        self.renderers[TaskList]       = self.render_task_list
        self.renderers[ListBlock]      = self.render_list_block
        self.renderers[ListItem]       = self.render_list_item
        self.renderers[CodeBlock]      = self.render_code_block
        self.renderers[BlockQuote]     = self.render_block_quote
        self.renderers[Callout]        = self.render_callout
        self.renderers[Card]           = self.render_card
        self.renderers[LinkList]       = self.render_link_list
        self.renderers[Table]          = self.render_table
        self.renderers[Paragraph]      = self.render_paragraph
        self.renderers[InlineText]     = self.render_text_element
        self.renderers[HtmlComment]    = self.render_html_comment

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
        args = {}
        if heading.hid is not None:
            args['id'] = heading.hid
        return HtmlTemplates.heading(heading.weight, rendered_title, **args) 

    def render_list_block(self, list_block: ListBlock, **kwargs) -> str:
        list_elems = '\n'.join(self.render_element(elem) for elem in list_block.elements)
        if list_block.list_type == ListType.ORDERED:
            return HtmlTemplates.ordered_list(list_elems, **kwargs) 
        else:
            return HtmlTemplates.unordered_list(list_elems, **kwargs) 

    def render_list_item(self, li, **kwargs) -> str:
        rendered_text = self.render_text_element(li.text)
        return HtmlTemplates.list_item(rendered_text, **kwargs)

    def render_task_list(self, t_list: TaskList) -> str:
        list_items = '\n'.join(self.render_task_list_item(li) for li in t_list.items)
        return HtmlTemplates.unordered_list(list_items, cls="task-list")

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

    def render_callout(self, callout: Callout) -> str:
        rendered_title = self.render_text_element(callout.title)
        rendered_text = "\n".join(self.render_element(elem) for elem in callout.elements)
        return HtmlTemplates.callout(callout.type, callout.symbol, rendered_title, rendered_text)

    def render_card(self, card:Card) -> str:
        card_body = "\n".join(self.render_element(elem) for elem in card.elements)
        return HtmlTemplates.card(card.title, card_body)

    def render_link_list(self, link_list:LinkList) -> str:
        list_items = []
        for p in link_list.elements:
            for elem in p.text_element.elements:
                if isinstance(elem, RawText) and len(elem.raw_text().strip()) > 0:
                    list_items.append(HtmlTemplates.list_item(elem.raw_text().strip()))
                elif isinstance(elem, Hyperlink):
                    list_items.append(self.render_hyperlink(elem, lambda t: f"<li>{t}</li>"))
        return HtmlTemplates.unordered_list("\n".join(list_items), cls="link-list", style="--col_accent: var(--col_accent1)") 

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
            if isinstance(text, BoldItalicsText):
                return HtmlTemplates.bold(HtmlTemplates.italics(rendered_children))
            if isinstance(text, BoldText):
                return HtmlTemplates.bold(rendered_children)
            if isinstance(text, ItalicsText):
                return HtmlTemplates.italics(rendered_children)
            if isinstance(text, CodeText):
                return HtmlTemplates.code(rendered_children)
            if isinstance(text, LatexMath):
                return HtmlTemplates.latex(rendered_children)
            if isinstance(text, StrikethroughText):
                return HtmlTemplates.delete(rendered_children)
            if isinstance(text, HighlightText):
                return HtmlTemplates.mark(rendered_children)
            return rendered_children

        return str(text)

    def render_html_comment(self, comment: HtmlComment) -> str:
        return str(comment)

    def render_tag(self, tag: Tag) -> str:
        return HtmlTemplates.a("#" + tag.title, "", cls="tag red-tag")

    def is_relative(self, addr):
        for pattern in [ 'http', 'www', 'mailto', '#' ]:
            if addr.startswith(pattern):
                return False
        return True
    
    def render_hyperlink(self, link: Hyperlink, wrap_text: callable = None) -> str:
        link_text = self.render_text_element(link.text)
        if wrap_text:
            link_text = wrap_text(link_text)
        link_addr = link.addr
        if self.is_relative(link_addr):
            link_addr = self.url_mapper(link_addr)
        args = { }
        if link.title is not None:
            args['title'] = link.title
        return HtmlTemplates.a(link_text, link_addr, **args)
    
    def render_image(self, img: Image) -> str:
        img_url = img.filename
        if self.is_relative(img_url):
            img_url = self.url_mapper(img_url)
        args = { }
        if img.width is not None:
            img_width = img.width if '%' in img.width else img.width + "px"
            args['style'] = f'width: {img_width};'
        if img.title is not None:
            args['title'] = img.title
        return HtmlTemplates.img(img_url, img.alt_text, **args)

    def render_linked_image(self, img: LinkedImage) -> str:
        rendered_image = self.render_image(img)

        link_addr = img.addr
        if self.is_relative(link_addr):
            link_addr = self.url_mapper(link_addr)

        return HtmlTemplates.a(rendered_image, link_addr)

    def render_document(self, title:str, elements:list, css_files:list=[], js_files:list=[]):
        html = self.render_markdown_elements(elements)
        css = self.read_css_files(css_files)
        js = self.read_js_files(js_files)
        return HtmlTemplates.document_inlined(title, css, js, html)

    def read_css_files(self, css_files):
        css = []
        for css_file in css_files:
            if not os.path.exists(css_file):
                print(f"CSS File {css_file} does not exist", file=sys.stderr)
                continue
            with open(css_file, 'r') as f:
                css.append(f.read())
        return "\n".join(css)

    def read_js_files(self, js_files):
        js = []
        for js_file in js_files:
            if not os.path.exists(js_file):
                print(f"JavaScript File {js_file} does not exist", file=sys.stderr)
                continue
            with open(js_file, 'r') as f:
                js.append(f.read())
        return "\n".join(js)



