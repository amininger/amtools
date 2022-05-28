import os
import re

from amtools import LineReader, FileReader


class fsutil:
    """ Contains static methods for interacting with the file system """

    @staticmethod
    def filename2title(filename: str):
        """ Takes the file name and makes it into a more readable title """
        name = os.path.splitext(filename)[0]
        words = re.split('[-_]', name)
        return ' '.join(word.capitalize() for word in words)
    
    @staticmethod
    def find_file(dir_path: str, name: str) -> str:
        """ Given a directory and a file name, try to find an existing file that matches it """
        if not os.path.isdir(dir_path):
            return None
        
        for f in os.listdir(dir_path):
            if not f.startswith('.') and os.path.splitext(f)[0] == name:
                return os.path.join(dir_path, f)

        return None

    @staticmethod
    def get_files_in_dir(dir_path: str) -> dict:
        """ Returns all the files in the directory that match valid extensions """
        files = {}
        for f in os.listdir(dir_path):
            if f.startswith('.'):
                continue
            parts = os.path.splitext(f)
            if parts[1] in [ ".md", ".txt" ]:
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
        except FileNotFoundError:
            return None


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



