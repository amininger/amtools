import re 

from amtools.markdown.elements import *
from .html_templates import HtmlTemplates

NL_PLACEHOLDER = '_#!_NL_!#_'

def replace_link(text :str):
    close_br = text.index(']')
    link_text = text[1:close_br]
    link_addr = text[close_br+2:-1]
    return HtmlTemplates.a(link_text, link_addr)


def replace_pattern(text, pattern :str, del_front :int, del_end :int, inner_replace=lambda x: x):
    # Will replace all occurences of the given pattern in the given text and return the result
    # Assumes the pattern is of the form FRONT_PATTERN INNER_TEXT END_PATTERN (e.g. **bold text**)
    # text = string
    # pattern = regex pattern
    # del_front is the # of characters to delete at the front of the matching text
    # del_end is the # of characters to delete at the end of the matching text
    # inner_replace is an optional function mapping the inner text to some other output
    result = ""
    match = re.search(pattern, text)
    while match is not None:
        s, e   = match.start(), match.end()
        before = text[:s]
        inner  = text[s + del_front : e - del_end]
        after  = text[e:]

        result += before 
        text   = inner_replace(inner) + after
        match = re.search(pattern, text)
    result += text
    return result


class HtmlRenderer:

    def render_markdown_elements(self, elements: list) -> str:
        """ Renders a list of markdown elements into a string of html """
        body = '\n'.join(self.render_element(el) for el in elements)
        html = body.replace(NL_PLACEHOLDER, '\n')
        return html
    
    def render_element(self, elem):
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
        return ""


    def render_horizontal_rule(self, hr: HorizontalRule):
        return HtmlTemplates.hr()

    def render_heading(self, heading: Heading):
        rendered_title = self.render_inline_text(heading.title)
        return HtmlTemplates.heading(heading.weight, rendered_title) 

    def render_bulleted_list(self, b_list: BulletedList):
        list_items = '\n'.join(self.render_list_item(li) for li in b_list.items)
        return HtmlTemplates.unordered_list(list_items) 

    def render_numbered_list(self, n_list: NumberedList):
        list_items = '\n'.join(self.render_list_item(li) for li in n_list.items)
        return HtmlTemplates.ordered_list(list_items) 

    def render_list_item(self, li: str):
        rendered_text = self.render_inline_text(li)
        return HtmlTemplates.list_item(rendered_text)
    
    def render_code_block(self, block: CodeBlock):
        compacted_block = block.text.replace('\n', NL_PLACEHOLDER)
        return HtmlTemplates.code(compacted_block)

    def render_paragraph(self, par: Paragraph):
        rendered_text = self.render_inline_text(par.text)
        return HtmlTemplates.p(rendered_text)


    def render_inline_text(self, text):
        """ Takes the given text and does inline substitutions (e.g. bold/italics) """
        html = text
        # Bold
        html = replace_pattern(html, r"\*\*[^*]+\*\*", 2, 2, HtmlTemplates.bold)
        # Italics
        html = replace_pattern(html, r"_[^_]+_", 1, 1, HtmlTemplates.italics)
        ## Special [[ ]] blocks
        #html = replace_pattern(html, r"\[\[[^[]+\]\]", (2, '<span class="conj-label">'), (2, '</span>'), 
        #        lambda text: text.replace('/', '</span><span class="conj-label">'))
        # Inline Code ` `
        html = replace_pattern(html, r"`[^`]+`", 1, 1, lambda text: HtmlTemplates.span('inline-code', text))

        # Links [text](addr)
        html = replace_pattern(html, r"\[[^]]*\]\([^)]*\)", 0, 0, replace_link)

        return html


