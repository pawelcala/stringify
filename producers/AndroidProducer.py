# PRODUCERS
import os
import xml.etree.ElementTree as ET
from xml.dom import minidom

from model.Base import Command
from utils.FileUtils import save_file
from utils.LogUtils import log_step


class Producer(Command):
    def execute(self):
        pass


class AndroidProducer(Producer):
    def __init__(self, google_doc_handler, google_doc_name, export_path=".", default_language="en",
                 xml_name="strings.xml"):

        self.xml_name = xml_name
        self.default_language = default_language
        self.export_path = export_path
        self.google_doc_name = google_doc_name
        self.google_doc_handler = google_doc_handler

    def execute(self):
        dictionary = self.google_doc_handler.read(self.google_doc_name)
        self._export(dictionary)

    def _export(self, dictionary):
        log_step("Exporting Android strings")
        cwd = os.getcwd()
        if self.export_path:
            try:
                os.makedirs(self.export_path, exist_ok=True)
            except Exception:
                pass
            os.chdir(self.export_path)

        for i, lang in enumerate(dictionary.languages):
            xml = ET.Element('resources')
            for key in dictionary.keys():
                value = dictionary.get_translation(key, lang)
                string_row = ET.SubElement(xml, 'string')
                string_row.set('name', key)
                string_row.text = value

            dom = minidom.parseString(ET.tostring(xml, 'utf-8'))
            pretty_dom = dom.toprettyxml()

            dir_name = "values".format(self.default_language) if self.default_language == lang else "values-{}".format(
                lang)
            save_file(pretty_dom, dir_name, self.xml_name)

        os.chdir(cwd)
