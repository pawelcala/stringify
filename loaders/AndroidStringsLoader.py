import re
import xml.etree.ElementTree as ET

from model.Base import DataLoader
from model.Models import Dictionary
from utils.FileUtils import find_files


class AndroidStringsLoader(DataLoader):
    def __init__(self, path, **kwargs):
        self.path = path
        self.filename = kwargs['xml_name'] if 'xml_name' in kwargs.keys() else 'strings.xml'
        self.default_language = kwargs['default_language'] if 'default_language' in kwargs.keys() else 'en'

    def execute(self):
        file_paths = find_files(path=self.path, filename_regex=self.filename)
        dictionary = Dictionary()
        for filepath in file_paths:
            language = self._decode_filepath_language(filepath)
            entries = self._decode_file_entries(filepath)

            if len(language.strip()) == 0:
                language = self.default_language

            for entry in entries:
                dictionary.add_translation(entry[0], language, entry[1])
        return dictionary

    def _decode_filepath_language(self, filepath):
        match = re.match(r'.*values([-a-z]{0,3})', filepath)
        if match:
            postfix = match.group(1)
            if len(postfix) == 3:
                postfix = postfix[-2:]
            else:
                postfix = self.default_language
        return postfix

    def _decode_file_entries(self, filepath):
        entries = []
        xml = ET.parse(filepath)
        root = xml.getroot()
        for child in root:
            if child.tag == 'string':
                key = child.get('name')
                value = ""
                for t in child.iter():
                    if t.tag == 'string':
                        value += t.text
                    else:
                        value += "<{}>{}</{}>".format(t.tag, t.text, t.tag)
                entries.append((key, value))
        return entries
