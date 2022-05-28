import re

from amtools import LineReader, FileReader
from amtools.markdown.elements import *

r_COMMENT       = re.compile(r"^//")
r_EMPTY_LINE    = re.compile(r"^[ \t]*$")
r_CODE_BLOCK    = re.compile(r"^```")
r_HEADING       = re.compile(r"^#{1,6} ")
r_HRULE         = re.compile(r"^[-=]{3,}$")
r_BULLETED_LIST = re.compile(r"^[*-] ")
r_NUMBERED_LIST = re.compile(r"^[0-9]{1,2}\. ")

class MarkdownParser:
    @staticmethod
    def parse_file(filename: str) -> list:
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
        

    def parse_markdown(self, line_reader: LineReader):
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
                    elements[-1].add_line(next_line)
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
                elements[-1].add_line(next_line)
            else:
                elements.append(Paragraph(next_line))
            line_reader.skip_line()

        return elements

    ################################################################
    # Line Elements - take up an entire line in the file

    def parse_line_elements(self, line: str):
        """ Tries to match the line against the known line elements
            If successful, consumes the line and returns the parsed element
            If no patterns match, returns None """

        if r_HEADING.match(line):
            return self.parse_heading(line)
        
        if r_HRULE.match(line):
            return HorizontalRule()

        return None


    def parse_heading(self, line: str) -> Heading:
        weight = 0
        while line.startswith('#'):
            weight += 1
            line = line[1:]

        title = line.strip()
        return Heading(weight, title)



    ##############################################################
    # Block Elements - take up multiple lines

    def parse_block_elements(self, line_reader: LineReader):
        """ Tries to match the next line against the known block elements
            If successful, consumes the block lines and returns the parsed element
            If no patterns match, returns None """

        next_line = line_reader.peek()

        if r_CODE_BLOCK.match(next_line):
            return self.parse_code_block(line_reader)

        if r_BULLETED_LIST.match(next_line):
            return self.parse_bulleted_list(line_reader)

        if r_NUMBERED_LIST.match(next_line):
            return self.parse_numbered_list(line_reader)

        return None

    def parse_code_block(self, line_reader: LineReader) -> CodeBlock:
        line_reader.skip_line()
        block_text = "\n".join(line_reader.read_lines_until('```', include_end=False))
        line_reader.skip_line()
        return CodeBlock(block_text)

    def parse_bulleted_list(self, line_reader: LineReader) -> BulletedList:
        items = []
        while not line_reader.at_end():
            next_line = line_reader.peek()
            if r_BULLETED_LIST.match(next_line):
                items.append(line_reader.read_line()[2:].strip())
            elif r_EMPTY_LINE.match(next_line):
                line_reader.skip_line()
            else:
                break
        
        return BulletedList(items)

    def parse_numbered_list(self, line_reader: LineReader) -> NumberedList:
        items = []
        while not line_reader.at_end():
            next_line = line_reader.peek()
            if r_NUMBERED_LIST.match(next_line):
                items.append(next_line[next_line.index('.')+2:].strip())
                line_reader.skip_line()
            elif r_EMPTY_LINE.match(next_line):
                line_reader.skip_line()
            else:
                break
        
        return NumberedList(items)

