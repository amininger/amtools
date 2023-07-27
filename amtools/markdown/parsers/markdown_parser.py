import re
from dataclasses import dataclass
from typing import Callable, List

from amtools import LineReader, FileReader, ListReader
from amtools.markdown.elements import *

r_COMMENT       = re.compile(r"^//")
r_EMPTY_LINE    = re.compile(r"^[ \t]*$")
r_INDENTED      = re.compile(r"^(\t|    )")
r_BOLD_ITALICS  = re.compile(r"\*\*\*([^*]+)\*\*\*")
r_BOLD          = re.compile(r"\*\*([^*]+)\*\*")
r_ITALICS       = re.compile(r"_([^_]+)_")
r_STRIKETHROUGH = re.compile(r"~~([^~]+)~~")
r_HIGHLIGHT     = re.compile(r"==([^=]+)==")
r_CODE          = re.compile(r"`([^`]+)`")
r_CODE2         = re.compile(r"``([^`]([^`]|`[^`])+)``")
r_LATEX_MATH    = re.compile(f"\$([^$]+)\$($|[^0-9$])")
r_TAG           = re.compile(r"^\#([-/\w]*[a-zA-Z][-/\w]*)\b")
r_TAG2          = re.compile(r"\s\#([-/\w]*[a-zA-Z][-/\w]*)\b")
r_LINK          = re.compile(r'\[([^][]*)\]\(([^)("\s]+)\s*("[^"]+")?\)')
r_INTERNAL_LINK = re.compile(r'\[\[([^][]*)\]\]\(([^)("\s]+)\s*("[^"]+")?\)')
r_ANGLE_LINK    = re.compile(r"<([^<>\s]+\.[^<>\s]+)>")
#r_INTERNAL_LINK = re.compile(r"\[\[([^][]*)\]\]")
#r_INLINE_IMAGE  = re.compile(r"!\[([^][]*)\]\(([^)(]+)\)")
#r_INLINE_IMAGE2 = re.compile(r"!\[\[([^][]*)\]\]")

r_HEADING       = re.compile(r"^(#{1,6}) ([^{]*)(\{\#[-\w]*[a-zA-Z][-\w]*\})?\s*$")
r_HRULE         = re.compile(r"^[-=_*]{3,}$")
r_IMAGE         = re.compile("!" + r_LINK.pattern)
r_IMAGE2        = re.compile("!" + r_INTERNAL_LINK.pattern)
r_IMAGE3        = re.compile("!\[\[([^][]*)\]\]")
r_LINKED_IMAGE  = re.compile("\[" + r_IMAGE.pattern + '\]\(([^)(]+)\)')
r_HTML_COMMENT  = re.compile(r"<!--(.*)-->")

r_TABLE         = re.compile(r"^\|([^|]+\|)+ *$")
r_TASK_LIST     = re.compile(r"^- \[[ ?xX]\] ")
r_BULLETED_LIST = re.compile(r"^[*-+] ")
r_NUMBERED_LIST = re.compile(r"^[0-9A-Z]{1,3}\. ")
r_CODE_BLOCK    = re.compile(r"^```\w*\s*$")
r_BLOCK_QUOTE   = re.compile(r"^> ")
r_CALLOUT_BLOCK = re.compile(r"^> \[!([-\w]+)\]\s*(.*)$")
r_CUSTOM_BLOCK  = re.compile(r"^> \[!!([-\w]+[^]]*)\]\s*$")

TASK_STATUS_SYMBOLS = { 'x': TaskItemStatus.COMPLETE, 'X': TaskItemStatus.COMPLETE, 
                        '?': TaskItemStatus.UNKNOWN,  ' ': TaskItemStatus.INCOMPLETE }

def get_indent(s):
    c = 0
    while c < len(s) and s[c] == '\t':
        c += 1
    return c

class ParsedArg:
    pass

class UnparsedArg:
    pass

@dataclass 
class BlockElementMatcher:
    pattern: re.Pattern
    parser: Callable[[re.Match, LineReader], MarkdownElement]

@dataclass 
class LineElementMatcher:
    pattern: re.Pattern
    parser: Callable[[str], MarkdownElement]

class TextElementMatcher:
    def __init__(self, pattern: re.Pattern, element: MarkdownElement, *args):
        self.pattern = pattern
        self.element = element
        self.args = args


def split_match(text: str, re_match: re.Match) -> (str, List[str], str):
    s, e   = re_match.start(), re_match.end()
    before = text[:s]
    inner  = re_match.groups()
    after  = text[e:]
    return (before, inner, after)

class MarkdownParser:
    @staticmethod
    def parse_string(markdown: str) -> List[MarkdownElement]:
        """ Parses the given markdown in the string and returns a list of elements """
        reader = ListReader(markdown.split('\n'))
        parser = MarkdownParser()
        return parser.parse_markdown(reader)

    @staticmethod
    def parse_file(filename: str) -> List[MarkdownElement]:
        """ Parses the given markdown file and returns a list of elements """
        try:
            # Skip meta block at the top
            reader = FileReader(filename)
            if reader.peek().strip() == '---':
                reader.skip_line()
                reader.read_lines_until('---')

            parser = MarkdownParser()
            return parser.parse_markdown(reader)
        except FileNotFoundError:
            return None
        
    def __init__(self):
        self.block_matchers = [ ]
        self.block_matchers.append(BlockElementMatcher(r_CUSTOM_BLOCK, self.parse_custom_block))
        self.block_matchers.append(BlockElementMatcher(r_CALLOUT_BLOCK, self.parse_callout_block))
        self.block_matchers.append(BlockElementMatcher(r_CODE_BLOCK,    self.parse_code_block))
        self.block_matchers.append(BlockElementMatcher(r_BLOCK_QUOTE,   self.parse_block_quote))
        self.block_matchers.append(BlockElementMatcher(r_TASK_LIST,     self.parse_task_list))
        self.block_matchers.append(BlockElementMatcher(r_BULLETED_LIST, self.parse_bulleted_list))
        self.block_matchers.append(BlockElementMatcher(r_NUMBERED_LIST, self.parse_numbered_list))
        self.block_matchers.append(BlockElementMatcher(r_TABLE,         self.parse_table))

        self.line_matchers = [ ]
        self.line_matchers.append(LineElementMatcher(r_EMPTY_LINE, self.skip_line))
        self.line_matchers.append(LineElementMatcher(r_COMMENT, self.skip_line))
        self.line_matchers.append(LineElementMatcher(r_HEADING, self.parse_heading))
        self.line_matchers.append(LineElementMatcher(r_HRULE,   self.parse_hrule))
        self.line_matchers.append(LineElementMatcher(r_LINKED_IMAGE, self.parse_linked_image))
        self.line_matchers.append(LineElementMatcher(r_IMAGE,   self.parse_image))
        self.line_matchers.append(LineElementMatcher(r_IMAGE2,  self.parse_image))
        self.line_matchers.append(LineElementMatcher(r_IMAGE3,  self.parse_embedded_image))
        self.line_matchers.append(LineElementMatcher(r_HTML_COMMENT, self.parse_html_comment))

        self.text_matchers = [ ]
        #self.text_matchers.append(TextElementMatcher(r_INLINE_IMAGE, Image, UnparsedArg))
        #self.text_matchers.append(TextElementMatcher(r_INLINE_IMAGE2, Image, UnparsedArg))
        self.text_matchers.append(TextElementMatcher(r_LINK, Hyperlink, ParsedArg, UnparsedArg, UnparsedArg))
        self.text_matchers.append(TextElementMatcher(r_INTERNAL_LINK, Hyperlink, ParsedArg, UnparsedArg, UnparsedArg))
        self.text_matchers.append(TextElementMatcher(r_ANGLE_LINK, Hyperlink, UnparsedArg))
        self.text_matchers.append(TextElementMatcher(r_TAG, Tag, UnparsedArg))
        self.text_matchers.append(TextElementMatcher(r_TAG2, Tag, UnparsedArg))
        self.text_matchers.append(TextElementMatcher(r_LATEX_MATH, LatexMath, UnparsedArg))
        self.text_matchers.append(TextElementMatcher(r_BOLD_ITALICS, BoldItalicsText, ParsedArg))
        self.text_matchers.append(TextElementMatcher(r_ITALICS, ItalicsText, ParsedArg))
        self.text_matchers.append(TextElementMatcher(r_BOLD, BoldText, ParsedArg))
        self.text_matchers.append(TextElementMatcher(r_STRIKETHROUGH, StrikethroughText, ParsedArg))
        self.text_matchers.append(TextElementMatcher(r_HIGHLIGHT, HighlightText, ParsedArg))
        self.text_matchers.append(TextElementMatcher(r_CODE2, CodeText, UnparsedArg))
        self.text_matchers.append(TextElementMatcher(r_CODE, CodeText, UnparsedArg))

    def close_paragraph(self, paragraph, elements):
        if paragraph is not None:
            elements.append(paragraph)
            paragraph.text_element = self.parse_inline_text(paragraph.text)
        return None

    def parse_markdown(self, line_reader: LineReader) -> List[MarkdownElement]:
        """ Parses all the lines in the given line_reader as markdown
            and returns a list of markdown Elements """

        elements = []
        current_paragraph = None

        while not line_reader.at_end():
            # Peek at the next line in the file
            next_line = line_reader.peek()

            # See if the line matches a line element
            if line_elem := self.parse_line_elements(next_line):
                current_paragraph = self.close_paragraph(current_paragraph, elements)
                if not isinstance(line_elem, EmptyElement):
                    elements.append(line_elem)

            # See if the line matches a block element
            elif block_elem := self.parse_block_elements(line_reader):
                current_paragraph = self.close_paragraph(current_paragraph, elements)
                elements.append(block_elem)
                continue

            # Otherwise, it is a text element, add to a paragraph
            elif current_paragraph is None:
                current_paragraph = Paragraph(next_line)
            else:
                current_paragraph.add_text(next_line)

            line_reader.skip_line()

        current_paragraph = self.close_paragraph(current_paragraph, elements)
        return elements

    ################################################################
    # Line Elements - take up an entire line in the file

    def parse_line_elements(self, line: str):
        """ Tries to match the line against the known line elements
            If successful, consumes the line and returns the parsed element
            If no patterns match, returns None """

        for matcher in self.line_matchers:
            re_match = matcher.pattern.match(line)
            if re_match is not None:
                return matcher.parser(line, re_match)
        return None

    # Tells the parser to skip this line (a comment, for example)
    def skip_line(self, line: str, re_match: re.Match) -> EmptyElement:
        return EmptyElement()

    def parse_hrule(self, line: str, re_match: re.Match) -> HorizontalRule:
        return HorizontalRule()

    def parse_heading(self, line: str, re_match: re.Match) -> Heading:
        weight = len(re_match.group(1))
        title = self.parse_inline_text(re_match.group(2))
        hid = re_match.group(3)
        if hid is not None:
            hid = hid[2:-1] # Remove braces and # symbol
        return Heading(weight, title, hid)

    def parse_embedded_image(self, line: str, re_match: re.Match) -> Image:
        info = re_match.groups()[0]
        filename = info
        if "|" in info:
            filename = info.split("|")[0]

        return Image(info, filename, filename.split('.')[0])

    def parse_image(self, line: str, re_match: re.Match) -> Image:
        alt_text, filename, title = re_match.groups()
        if title is not None:
            title = title[1:-1] # Remove quotes
        return Image(alt_text, filename, title)

    def parse_linked_image(self, line: str, re_match: re.Match) -> Image:
        alt_text, filename, title, addr = re_match.groups()
        if title is not None:
            title = title[1:-1] # Remove quotes
        return LinkedImage(alt_text, filename, title, addr)

    def parse_html_comment(self, line: str, re_match: re.Match) -> RawText:
        inner_text, = re_match.groups()
        return HtmlComment(inner_text)

    ##############################################################
    # Block Elements - take up multiple lines

    def parse_block_elements(self, line_reader: LineReader):
        """ Tries to match the next line against the known block elements
            If successful, consumes the block lines and returns the parsed element
            If no patterns match, returns None """

        next_line = line_reader.peek()

        for matcher in self.block_matchers:
            re_match = matcher.pattern.match(next_line)
            if re_match is not None:
                return matcher.parser(re_match, line_reader)

        return None

    def parse_code_block(self, re_match: re.Match, line_reader: LineReader) -> CodeBlock:
        """ Reads until the end of the code block and returns a CodeBlock object """
        open_line = line_reader.read_line()
        block_text = "\n".join(line_reader.read_lines_until('```', include_end=False))
        line_reader.skip_line()
        return CodeBlock(block_text, open_line[3:])

    def parse_block_quote(self, re_match: re.Match, line_reader: LineReader) -> BlockQuote:
        """ Reads until the end of the block quote and returns a BlockQuote object """
        lines = []
        while not line_reader.at_end() and r_BLOCK_QUOTE.match(line_reader.peek()):
            lines.append(line_reader.read_line()[2:])
        block_reader = ListReader(lines)
        block_elems = self.parse_markdown(block_reader)
        return BlockQuote(block_elems)

    def parse_callout_block(self, re_match: re.Match, line_reader: LineReader) -> Callout:
        callout_type = re_match.group(1).lower()

        alt_title = re_match.group(2)
        if alt_title is not None:
            alt_title = alt_title.strip()
            if len(alt_title) == 0:
                alt_title = None
            else:
                alt_title = self.parse_inline_text(alt_title)

        line_reader.skip_line()
        block_quote = self.parse_block_quote(re_match, line_reader)
        return Callout(callout_type, alt_title, block_quote.elements)

    def parse_custom_block(self, re_match: re.Match, line_reader: LineReader) -> MarkdownElement:
        block_info = re_match.group(1).split("|")
        block_type = block_info[0].lower()
        line_reader.skip_line()

        block_quote = self.parse_block_quote(re_match, line_reader)
        return make_custom_block(block_type, block_quote.elements, *block_info[1:])

    def parse_task_list(self, re_match: re.Match, line_reader: LineReader) -> TaskList:
        """ Reads until the end of the task list block and 
            creates and returns a TaskList object """
        items = []
        while not line_reader.at_end():
            next_line = line_reader.peek()
            if r_TASK_LIST.match(next_line):
                item_text = self.parse_inline_text(next_line[6:].strip())
                item_status = TASK_STATUS_SYMBOLS.get(next_line[3], TaskItemStatus.INCOMPLETE)
                items.append(TaskItem(item_text, item_status))
            elif not r_EMPTY_LINE.match(next_line):
                # If we hit a different non-empty line, exit
                break
            line_reader.skip_line()
        
        return TaskList(items)

    def parse_bulleted_list(self, re_match: re.Match, line_reader: LineReader) -> ListBlock:
        """ Reads until the end of the bulleted list block and 
            creates and returns a ListBlock object """
        return self.parse_list_block(ListType.UNORDERED, r_BULLETED_LIST, line_reader)

    def parse_numbered_list(self, re_match: re.Match, line_reader: LineReader) -> ListBlock:
        """ Reads until the end of the numbered list block and 
            creates and returns a ListBlock object """
        return self.parse_list_block(ListType.ORDERED, r_NUMBERED_LIST, line_reader)

    def parse_list_block(self, list_type: ListType, line_pattern: re.Pattern, 
                         line_reader: LineReader) -> ListBlock:
        """ Reads until the end of the list block and return a ListBlock object """
        elements = []
        inner_lines = []
        while not line_reader.at_end():
            # Keep reading until we hit something that doesn't belong in the list
            next_line = line_reader.peek()
            if line_pattern.match(next_line):
                # Normal ListItem
                if len(inner_lines) > 0:
                    # If we are closing an inner block, parse and add it
                    elements.extend(self.parse_markdown(ListReader(inner_lines)))
                    inner_lines = []

                item_text = re.sub(line_pattern, '', next_line)
                item_text = self.parse_inline_text(item_text)
                elements.append( ListItem(list_type, item_text) )

            elif r_EMPTY_LINE.match(next_line):
                # Ignore empty lines
                pass

            elif r_INDENTED.match(next_line):
                # Read indented lines to parse later
                next_line = re.sub(r_INDENTED, '', next_line)
                inner_lines.append(next_line)

            else:
                # If we hit a non-empty line, exit
                break

            line_reader.skip_line()
        
        if len(inner_lines) > 0:
            elements.extend(self.parse_markdown(ListReader(inner_lines)))
        return ListBlock(list_type, elements)


    def parse_table(self, re_match: re.Match, line_reader: LineReader) -> Table:
        headings = line_reader.read_line().split("|")[1:-1]
        table = Table([self.parse_inline_text(heading.strip()) for heading in headings])

        line_reader.skip_line()

        while not line_reader.at_end():
            next_line = line_reader.peek()
            if not r_TABLE.match(next_line):
                break
            cols = line_reader.read_line().split("|")[1:-1]
            table.add_row([ self.parse_inline_text(col.strip()) for col in cols ])

        return table

    ##############################################################
    # Inline Text Elements - formatted text

    def parse_inline_text(self, text: str) -> InlineText:
        """ Will parse a blob of text with inline formatting elements, 
            such as bold, italics, inline code, links, etc """

        for matcher in self.text_matchers:
            re_match = re.search(matcher.pattern, text)
            if re_match is not None:
                return self.parse_matched_inline_text(text, re_match, matcher)

        return RawText(text)

    def collect_matched_args(self, inner_matches, arg_info): 
        args = []
        for i, mat in enumerate(inner_matches):
            if i < len(arg_info):
                if arg_info[i] is ParsedArg:
                    args.append(self.parse_inline_text(mat))
                else:
                    args.append(mat)
        while len(args) < len(arg_info):
            args.append(None)
        return args

    def parse_matched_inline_text(self, text: str, re_match: re.Match, matcher: TextElementMatcher) -> InlineText:
        """ Given a regex match in a text string, splits into the three parts
                (before, inner, after)
            and parses each one before returning an InlineText containing all three """
        before, inner_matches, after = split_match(text, re_match)
        element_args = self.collect_matched_args(inner_matches, matcher.args)

        return InlineText(
            self.parse_inline_text(before), 
            matcher.element(*element_args),
            self.parse_inline_text(after) 
        )



