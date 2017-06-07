from formatter.android_formatters import AndroidToDictionary
from googledocs.GoogleDocsHandler import GoogleDocsHandler
from importers.language_decoders import AndroidLanguagePathDecoder
from importers.localizable_finder import LocalizableFinder
from model.Models import Dictionary


class AndroidToDocs:
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
            atd = AndroidToDictionary(dictionary)
            atd.format(open(file_path), language)

        google_doc_handler = GoogleDocsHandler(self.google_credentials_path)
        google_doc_handler.write(self.google_sheet_name, dictionary)

    def langage_path_decoder(self, path):
        return AndroidLanguagePathDecoder(path, self.default_lang).decode()
