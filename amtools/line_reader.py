import abc

class LineReader:
    """ LineReader: Abstract Interface for reading text line by line """

    def __init__(self):
        """ Note: Call super __init__ after the reader is set up """
        self.peeked_line = self._next_line()

    def at_end(self) -> bool:
        """ Returns true if the reader is at the end of the text """
        return self.peeked_line is None

    def peek(self) -> str:
        """ Returns the next line in the reader without advancing
                (or None if at end) """
        return self.peeked_line

    def skip_line(self) -> None:
        """ Moves the reader forward one line """
        if self.peeked_line is not None:
            self.peeked_line = self._next_line()

    def read_line(self, skip_empty=False) -> str:
        """ Returns the next line in the reader 
                (or None if at the end)
            skip_empty: If true, will skip whitespace lines """

        if skip_empty:
            while self.peeked_line is not None and self.peeked_line.strip() == "":
                self.peeked_line = self._next_line()
        
        next_line = self.peeked_line
        self.peeked_line = self._next_line()
        return next_line

    def read_lines(self, num_lines=1, skip_empty=False) -> [str]:
        """ Returns a list of strings, the next num_lines in the reader
                (Or fewer if the end of the file is reached)
            skip_empty: If True, will not include empty whitespace lines """
        lines = []
        while not self.at_end() and len(lines) < num_lines:
            next_line = self.read_line(skip_empty=skip_empty)
            if next_line is not None:
                lines.append(next_line)
        return lines

    def read_lines_until(self, *patterns :str, include_end=True) -> [str]:
        """ Will keep reading lines until a line starts with one of the given patterns
            include_end: if False, will not read the matching line and append it to the list
        """
        lines = []
        while self.peeked_line is not None:
            if any(self.peeked_line.startswith(p) for p in patterns):
                break
            lines.append(self.peeked_line)
            self.peeked_line = self._next_line()

        if include_end and self.peeked_line is not None:
            lines.append(self.peeked_line)
            self.peeked_line = self._next_line()

        return lines

    @abc.abstractmethod
    def _next_line(self) -> str:
        """ reads and returns the next line (or None if at end) """
        return



class ListReader(LineReader):
    """ ListReader: Implements the LineReader interface over a list of strings """

    def __init__(self, lines: list):
        """ lines: list of strings """
        self.index = 0
        self.lines = lines
        self.num_lines = len(lines)
        super().__init__()

    def _next_line(self) -> str:
        if self.index >= self.num_lines:
            return None
        self.index += 1
        return self.lines[self.index-1]


class FileReader(LineReader):
    """ FileReader: Implements the Line Reader interface for a text file """

    def __init__(self, filename :str):
        """ filename: the name of the file to open 
            Note: will throw FileNotFoundException """
        self.filename = filename
        self.file = open(filename, 'r', encoding='utf-8')
        self.open_file = True
        super().__init__()

    def _next_line(self) -> str:
        if self.open_file is False:
            return None

        next_line = self.file.readline()
        if next_line == '':
            self._close()
            return None

        return next_line[:-1]
    
    def _close(self) -> None:
        """ Closes the file handle """
        self.file.close()
        self.open_file = False
        self.peeked_line = None

