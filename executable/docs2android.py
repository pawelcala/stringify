from xml.dom import minidom
from xml.etree import ElementTree
from googledocs.googledocs import GoogleDocsHandler
from model.models import Dictionary


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

        formatted_data = dict()
        for language in dictionary.languages:
            language_data = dta.format(language)
            formatted_data.update({language: language_data})

        print(formatted_data)


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
