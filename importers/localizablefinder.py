import re

from model.Models import Dictionary
from utils.FileUtils import find_files


class LocalizableFinder:
    def __init__(self, directory, filename_regex, default_language='en'):
        self.default_language = default_language
        self.filename_regex = filename_regex
        self.directory = directory

    def find(self):
        file_paths = find_files(path=self.directory, filename_regex=self.filename_regex)
        files_languages_list = list()
        for filepath in file_paths:
            language = self._decode_filepath_language(filepath)
            if language:
                files_languages_list.append((filepath, language))
        return files_languages_list

    def _decode_filepath_language(self, filepath):
        for decoder in (self._decode_language_android, self._decode_language_swift):
            language = decoder(filepath)
            if language:
                return language
        return None

    def _decode_language_android(self, filepath):
        match = re.match(r'.*values([-a-z]{0,3})', filepath)
        if match:
            postfix = match.group(1)
            if len(postfix) == 3:
                postfix = postfix[-2:]
            else:
                postfix = self.default_language
            return postfix
        return None

    def _decode_language_swift(self, filepath):
        match = re.match(r'(.*)\.lproj', filepath)
        if match:
            prefix = match.group(1)
            if len(prefix) > 2:
                prefix = prefix[-2:]
            return prefix
        return None
