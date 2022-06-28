import os
import re

from amtools import LineReader, FileReader, ListReader

class fsutil:
    """ Contains static methods for interacting with the file system """

    @staticmethod
    def filename2title(filename: str) -> str:
        """ Takes the file name and makes it into a more readable title """
        name = os.path.splitext(filename)[0]
        words = re.split('[-_]', name)
        return ' '.join(word.capitalize() for word in words)

    @staticmethod
    def simplify_path(path: str) -> str:
        parts = path.split("/")
        while '.' in parts:
            parts.remove('.')
        changes = True
        while changes:
            changes = False
            for i in range(1, len(parts)):
                if parts[i] == ".." and parts[i-1] != "" and parts[i-1] != "..":
                    parts.pop(i)
                    parts.pop(i-1)
                    changes = True
                    break
        return '/'.join(parts)

    
    @staticmethod
    def find_file(dir_path: str, name: str) -> str:
        """ Given a directory and a file name, try to find an existing file that matches it """
        if not os.path.isdir(dir_path):
            return None

        if os.path.exists(os.path.join(dir_path, name)):
            return name
        
        for f in os.listdir(dir_path):
            if f.replace(' ', '_') == name:
                return f

        return None

    @staticmethod
    def get_files_in_dir(dir_path: str, valid_extensions=None) -> dict:
        """ Returns all the files in the directory that match valid extensions """
        files = {}
        if valid_extensions is None:
            valid_extensions = [ ".md", ".txt" ]
        for f in os.listdir(dir_path):
            if f.startswith('.'):
                continue
            parts = os.path.splitext(f)
            if parts[1] in valid_extensions:
                files[parts[0]] = os.path.join(dir_path, f)
        return files

    @staticmethod
    def read_file_metadata(filename: str):
        """ Reads the yaml metadata at the top of the given file

            filename: The file to read the metadata for
            Returns a dictionary of metadata values, or None if the file does not exist
        """
        try:
            line_reader = FileReader(filename)
            return fsutil.parse_metadata(line_reader)
        except UnicodeDecodeError:
            # Binary file type
            return { }


    @staticmethod
    def parse_metadata(line_reader: LineReader):
        """ Will check if the line_reader is at a --- line 
            If so, reads until the end --- line and 
            parses the metadata between into a dictionary """
        metadata = {}
        first_line = line_reader.read_line(skip_empty=True)
        if first_line is not None and first_line.strip() == "---":
            metablock = line_reader.read_lines_until("---")
            if not metablock[-1].startswith("---"):
                return {}

            for line in metablock:
                # looks for lines of the form key: 'value'
                i = line.find(':')
                if i > 0:
                    metadata[line[:i]] = line[i+1:].replace("'", "").strip()

        return metadata

    @staticmethod
    def remove_metadata(text: str):
        lines = text.split('\n')
        i = 0
        while i < len(lines) and lines[i].strip() == "":
            i += 1
        if i >= len(lines) or lines[i].strip() != "---":
            return text
        i += 1
        while i < len(lines) and lines[i].strip() != "---":
            i += 1
        if i == len(lines):
            return text
        return "\n".join(lines[i+1:])

