import re

from model.Base import DataLoader, NotFoundException
from model.Models import Dictionary
from utils.FileUtils import find_files


class IOSStringsLoader(DataLoader):
    def __init__(self, path, **kwargs):
        self.path = path
        self.filename = kwargs['filename'] if 'filename' in kwargs.keys() else 'Localizable.strings'

    def execute(self):
        filepaths = find_files(path=self.path, filename_regex=self.filename)
        dictionary = Dictionary()

        for filepath in filepaths:
            language = self._decode_filepath_language(filepath)
            entries = self._decode_file_entries(filepath)

            for key, word in entries:
                dictionary.add_translation(key, language, word)

        return dictionary

    def _decode_filepath_language(self, path):
        match = re.match(r"""(.*)\.lproj""", path)
        if match:
            prefix = match.group(1)
            if len(prefix) > 2:
                prefix = prefix[-2:]
            return prefix
        else:
            raise NotFoundException

    def _decode_file_entries(self, filepath):
        entries = []
        file = open(filepath)

        for line in file:
            match = re.match(r'"(.*)".*=.*"(.*)";', line)
            if match:
                entries.append((match.group(1), match.group(2)))
        return entries
