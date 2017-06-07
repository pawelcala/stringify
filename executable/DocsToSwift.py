from formatter.ios_swift_formatters import DictionaryToSwift
from googledocs.GoogleDocsHandler import GoogleDocsHandler


class DocsToSwift:
    def __init__(self, settings):
        self.directory = settings.export_path()
        self.default_lang = settings.default_language()
        self.files_regex = settings.export_filename()

        self.google_credentials_path = settings.credentials_location()
        self.google_sheet_name = settings.google_doc_name()

    def execute(self):
        google_doc_handler = GoogleDocsHandler(self.google_credentials_path)
        dictionary = google_doc_handler.read(self.google_sheet_name)
        dta = DictionaryToSwift(dictionary)

        formatted_data = dict()
        for language in dictionary.languages:
            language_data = dta.format(language)
            formatted_data.update({language: language_data})

        print(formatted_data)
