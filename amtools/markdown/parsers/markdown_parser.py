import re
from dataclasses import dataclass
from typing import Callable, List

from amtools import LineReader, FileReader
from amtools.markdown.elements import *

r_COMMENT       = re.compile(r"^//")
r_EMPTY_LINE    = re.compile(r"^[ \t]*$")
r_BOLD          = re.compile(r"\*\*[^*]+\*\*")
r_ITALICS       = re.compile(r"_[^_]+_")
r_INLINE_CODE   = re.compile(r"`[^`]+`")
r_STRIKETHROUGH = re.compile(r"~~[^~]+~~")
r_HIGHLIGHT     = re.compile(r"==[^=]+==")
r_TAG           = re.compile(r"(^| )\#[a-zA-Z0-9_-]+")
r_LINK          = re.compile(r"\[[^]]*\]\([^)]+\)")

r_HEADING       = re.compile(r"^#{1,6} ")
r_HRULE         = re.compile(r"^[-=]{3,}$")
r_IMAGE         = re.compile(r"^!\[[^]]*\]\([^)]+\)")

r_TABLE         = re.compile(r"^\|([^|]+\|)+ *$")
r_TASK_LIST     = re.compile(r"^- \[[ ?xX]\] ")
r_BULLETED_LIST = re.compile(r"^[*-] ")
r_NUMBERED_LIST = re.compile(r"^[0-9]{1,2}\. ")
r_CODE_BLOCK    = re.compile(r"^```")
r_BLOCK_QUOTE   = re.compile(r"^> ")

TASK_STATUS_SYMBOLS = { 'x': TaskItemStatus.COMPLETE, 'X': TaskItemStatus.COMPLETE, 
                        '?': TaskItemStatus.UNKNOWN,  ' ': TaskItemStatus.INCOMPLETE }

@dataclass 
class BlockElementMatcher:
    pattern: re.Pattern
    parser: Callable[[LineReader], MarkdownElement]

@dataclass 
class LineElementMatcher:
    pattern: re.Pattern
    parser: Callable[[str], MarkdownElement]

@dataclass
class TextElementMatcher:
    pattern: re.Pattern
    element: type
    del_front: int
    del_end: int

def split_match(text: str, re_match: re.Match, del_front:int=0, del_end:int=0) -> (str, str, str):
    s, e   = re_match.start(), re_match.end()
    before = text[:s]
    inner  = text[s + del_front : e - del_end]
    after  = text[e:]
    return (before, inner, after)

class MarkdownParser:
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
        self.block_matchers.append(BlockElementMatcher(r_CODE_BLOCK,    self.parse_code_block))
        self.block_matchers.append(BlockElementMatcher(r_BLOCK_QUOTE,   self.parse_block_quote))
        self.block_matchers.append(BlockElementMatcher(r_TASK_LIST,     self.parse_task_list))
        self.block_matchers.append(BlockElementMatcher(r_BULLETED_LIST, self.parse_bulleted_list))
        self.block_matchers.append(BlockElementMatcher(r_NUMBERED_LIST, self.parse_numbered_list))
        self.block_matchers.append(BlockElementMatcher(r_TABLE,         self.parse_table))

        self.line_matchers = [ ]
        self.line_matchers.append(LineElementMatcher(r_HEADING, self.parse_heading))
        self.line_matchers.append(LineElementMatcher(r_HRULE,   self.parse_hrule))
        self.line_matchers.append(LineElementMatcher(r_IMAGE,   self.parse_image))

        self.text_matchers = [ ]
        self.text_matchers.append(TextElementMatcher(r_BOLD, BoldText, 2, 2))
        self.text_matchers.append(TextElementMatcher(r_ITALICS, ItalicsText, 1, 1))
        self.text_matchers.append(TextElementMatcher(r_INLINE_CODE, CodeText, 1, 1))
        self.text_matchers.append(TextElementMatcher(r_STRIKETHROUGH, StrikethroughText, 2, 2))
        self.text_matchers.append(TextElementMatcher(r_HIGHLIGHT, HighlightText, 2, 2))

    def parse_markdown(self, line_reader: LineReader) -> List[MarkdownElement]:
        """ Parses all the lines in the given line_reader as markdown
            and returns a list of markdown Elements """

        elements = []

        while not line_reader.at_end():
            # Peek at the next line in the file
            next_line = line_reader.peek()

            # Ignore comments
            if r_COMMENT.match(next_line):
                line_reader.skip_line()
                continue

            # If it is an empty line, only add to paragraphs
            if r_EMPTY_LINE.match(next_line):
                if elements and isinstance(elements[-1], Paragraph):
                    elements[-1].add_empty_line()
                line_reader.skip_line()
                continue

            # See if the line matches a line element
            line_elem = self.parse_line_elements(next_line)
            if line_elem is not None:
                elements.append(line_elem)
                line_reader.skip_line()
                continue

            # See if the line matches a block element
            block_elem = self.parse_block_elements(line_reader)
            if block_elem is not None:
                elements.append(block_elem)
                continue 

            # Otherwise, it is a text element, add to a paragraph
            if elements and isinstance(elements[-1], Paragraph):
                elements[-1].add_text(next_line)
            else:
                elements.append(Paragraph(next_line))
            line_reader.skip_line()

        for el in elements:
            if isinstance(el, Paragraph):
                self.parse_paragraph(el)

        return elements

    ################################################################
    # Line Elements - take up an entire line in the file

    def parse_line_elements(self, line: str):
        """ Tries to match the line against the known line elements
            If successful, consumes the line and returns the parsed element
            If no patterns match, returns None """

        for matcher in self.line_matchers:
            if matcher.pattern.match(line):
                return matcher.parser(line)
        return None

    def parse_hrule(self, line: str) -> HorizontalRule:
        return HorizontalRule()

    def parse_heading(self, line: str) -> Heading:
        weight = 0
        while line.startswith('#'):
            weight += 1
            line = line[1:]

        title = self.parse_inline_text(line.strip())
        return Heading(weight, title)

    def parse_image(self, line: str) -> Heading:
        close_br = line.index(']')
        alt_text = line[2:close_br]
        filename = line[close_br+2:-1]
        alt_parts = alt_text.split("|")
        params = None
        if len(alt_parts) == 2:
            alt_text, params = alt_parts

        return Image(filename, alt_text, params)



    ##############################################################
    # Block Elements - take up multiple lines

    def parse_block_elements(self, line_reader: LineReader):
        """ Tries to match the next line against the known block elements
            If successful, consumes the block lines and returns the parsed element
            If no patterns match, returns None """

        next_line = line_reader.peek()

        for matcher in self.block_matchers:
            if matcher.pattern.match(next_line):
                return matcher.parser(line_reader)

        return None

    def parse_code_block(self, line_reader: LineReader) -> CodeBlock:
        """ Reads until the end of the code block and returns a CodeBlock object """
        line_reader.skip_line()
        block_text = "\n".join(line_reader.read_lines_until('```', include_end=False))
        line_reader.skip_line()
        return CodeBlock(block_text)

    def parse_block_quote(self, line_reader: LineReader) -> BlockQuote:
        """ Reads until the end of the block quote and returns a BlockQuote object """
        block_quote = BlockQuote()
        while not line_reader.at_end() and r_BLOCK_QUOTE.match(line_reader.peek()):
            line = self.parse_inline_text(line_reader.read_line()[2:])
            block_quote.add_line(line)
        return block_quote

    def parse_task_list(self, line_reader: LineReader) -> TaskList:
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

    def parse_bulleted_list(self, line_reader: LineReader) -> BulletedList:
        """ Reads until the end of the bulleted list block and 
            creates and returns a BulletedList object """
        items = []
        while not line_reader.at_end():
            next_line = line_reader.peek()
            if r_BULLETED_LIST.match(next_line):
                item_text = next_line[2:].strip()
                items.append(self.parse_inline_text(item_text))
            elif not r_EMPTY_LINE.match(next_line):
                # If we hit a different non-empty line, exit
                break
            line_reader.skip_line()
        
        return BulletedList(items)

    def parse_numbered_list(self, line_reader: LineReader) -> NumberedList:
        """ Reads until the end of the numbered list block and 
            creates and returns a NumberedList object """
        items = []
        while not line_reader.at_end():
            next_line = line_reader.peek()
            if r_NUMBERED_LIST.match(next_line):
                item_text = next_line[next_line.index('.')+2:].strip()
                items.append(self.parse_inline_text(item_text))
            elif not r_EMPTY_LINE.match(next_line):
                # If we hit a different non-empty line, exit
                break
            line_reader.skip_line()
        
        return NumberedList(items)

    def parse_table(self, line_reader: LineReader) -> Table:
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

    def parse_paragraph(self, p: Paragraph) -> None:
        """ Will parse each line in the given paragraph as inline text """
        elements = [ self.parse_inline_text(line) for line in p.lines]
        if p.lines[-1] == '':
            elements = elements[:-1]
        p.set_elements(elements)

    def parse_inline_text(self, text: str) -> InlineText:
        """ Will parse a blob of text with inline formatting elements, 
            such as bold, italics, inline code, links, etc """

        for matcher in self.text_matchers:
            re_match = re.search(matcher.pattern, text)
            if re_match is not None:
                return self.parse_matched_inline_text(text, re_match, matcher)

        link_match = re.search(r_LINK, text)
        if link_match is not None:
            return self.parse_hyperlink(text, link_match)

        tag_match = re.search(r_TAG, text)
        if tag_match is not None:
            return self.parse_tag(text, tag_match)


        return RawText(text)

    def parse_matched_inline_text(self, text: str, re_match: re.Match, matcher: TextElementMatcher) -> InlineText:
        """ Given a regex match in a text string, splits into the three parts
                (before, inner, after)
            and parses each one before returning an InlineText containing all three """
        before, inner, after = split_match(text, re_match, matcher.del_front, matcher.del_end)
        return InlineText(
            self.parse_inline_text(before), 
            matcher.element(self.parse_inline_text(inner)),
            self.parse_inline_text(after) 
        )

    def parse_hyperlink(self, text: str, re_match: re.Match) -> InlineText:
        """ Given a regex match for a hyperlink, parses the before/after text
                and splits the inside into the text and address parts
            returns an InlineText containing the three parts """
        before, inner, after = split_match(text, re_match, 0, 0)

        close_br = inner.index(']')
        link_text = inner[1:close_br]
        link_addr = inner[close_br+2:-1]
        return InlineText(
            self.parse_inline_text(before), 
            Hyperlink(self.parse_inline_text(link_text), link_addr),
            self.parse_inline_text(after) 
        )

    def parse_tag(self, text: str, re_match: re.Match) -> InlineText:
        """ Given a regex match for a tag, parses the before/after text
                and creates a Tag with the inner part
            returns an InlineText containing the three parts """
        before, inner, after = split_match(text, re_match, 0, 0)
        tag_title = inner.strip()[1:]
        return InlineText(
            self.parse_inline_text(before), 
            Tag(tag_title), 
            self.parse_inline_text(after) 
        )



