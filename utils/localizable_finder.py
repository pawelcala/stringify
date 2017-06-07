from utils.FileUtils import find_files


class LocalizableFinder:
    def __init__(self, directory, filename_regex, default_language='en'):
        self.default_language = default_language
        self.filename_regex = filename_regex
        self.directory = directory

    def find(self, language_decoders=()):
        file_paths = find_files(path=self.directory, filename_regex=self.filename_regex)
        files_languages_list = list()
        for filepath in file_paths:
            language = self._decode_filepath_language(language_decoders, filepath)
            if language:
                files_languages_list.append((filepath, language))
        return files_languages_list

    def _decode_filepath_language(self, language_decoders, filepath):
        if language_decoders:
            for decoder in language_decoders:
                language = decoder(filepath)
                if language:
                    return language
        return self.default_language
