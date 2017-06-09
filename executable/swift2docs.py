import re
from googledocs.googledocs import GoogleDocsHandler
from model.models import Dictionary
from utils.language_decoders import IosSwiftLanguagePathDecoder
from utils.localizable_finder import LocalizableFinder


class SwiftToDocs:
    def __init__(self, settings):
        self.directory = settings.export_path()
        self.default_lang = settings.default_language()
        self.files_regex = settings.export_filename()

        self.google_credentials_path = settings.credentials_location()
        self.google_sheet_name = settings.google_doc_name()

    def execute(self):
        files_finder = LocalizableFinder(self.directory, self.files_regex, self.default_lang)
        files = files_finder.find(language_decoders=[self.langage_path_decoder])
        dictionary = Dictionary()
        for file_path, language in files:
            atd = SwiftImport(dictionary)
            atd.format(open(file_path), language)

        if dictionary.is_empty():
            raise Exception("Empty dictionary!")
        else:
            google_doc_handler = GoogleDocsHandler(self.google_credentials_path)
            google_doc_handler.write(self.google_sheet_name, dictionary)

    def langage_path_decoder(self, path):
        return IosSwiftLanguagePathDecoder(path).decode()


class SwiftImport:
    def __init__(self, dictionary):
        self.dictionary = dictionary

    def format(self, file, language):
        for line in file:
            match = re.match(r'"(.*)".*=.*"(.*)";', line)
            if match:
                self.dictionary.add_translation(match.group(1), language, match.group(2))
        return self.dictionary
