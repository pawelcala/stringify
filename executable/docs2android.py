import os
from xml.dom import minidom
from xml.etree import ElementTree
from googledocs.googledocs import GoogleDocsHandler
from model.models import Dictionary
from utils import file_utils
from utils.log_utils import log_step


class DocsToAndroid:
    def __init__(self, settings):
        self.directory = settings.export_path()
        self.default_lang = settings.default_language()
        self.files_regex = settings.export_filename()

        self.google_credentials_path = settings.credentials_location()
        self.google_sheet_name = settings.google_doc_name()

    def execute(self):
        google_doc_handler = GoogleDocsHandler(self.google_credentials_path)
        dictionary = google_doc_handler.read(self.google_sheet_name)
        dta = AndroidStringsExport(dictionary)

        for language in dictionary.languages:
            language_data = dta.format(language)
            self.save_language_data(language, language_data)

    def save_language_data(self, language, language_data):
        """
        TODO Refactoring!
        """
        dir = self.directory + os.sep + "values"
        if language != self.default_lang:
            dir += "-" + language

        file_utils.save_file(language_data, dir, self.files_regex)


class AndroidStringsExport:
    def __init__(self, dictionary=Dictionary(), use_pretty_xml=True):
        self.dictionary = dictionary
        self.use_pretty_xml = use_pretty_xml

    def format(self, language):
        xml_document = ElementTree.Element('resources')
        for key in self.dictionary.keys():
            string = self.dictionary.get_translation(key, language)
            string_element = ElementTree.SubElement(xml_document, 'string')
            string_element.set('name', key)
            string_element.text = string

        xml = ElementTree.tostring(xml_document, 'utf-8', method='html')
        if self.use_pretty_xml:
            dom = minidom.parseString(xml)
            xml = dom.toprettyxml()
        else:
            return xml.decode('utf-8')
        return xml
