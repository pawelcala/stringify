import xml.etree.ElementTree as ET
from xml.dom import minidom

from model.Models import Dictionary


class DictonaryToAndroid:
    def __init__(self, dictionary=Dictionary(), use_pretty_xml=True):
        self.dictionary = dictionary
        self.use_pretty_xml = use_pretty_xml

    def format(self, language):
        xml_document = ET.Element('resources')
        for key in self.dictionary.keys():
            string = self.dictionary.get_translation(key, language)
            string_element = ET.SubElement(xml_document, 'string')
            string_element.set('name', key)
            string_element.text = string

        xml = ET.tostring(xml_document, 'utf-8', method='html')
        if self.use_pretty_xml:
            dom = minidom.parseString(xml)
            xml = dom.toprettyxml()
        else:
            return xml.decode('utf-8')
        return xml


class AndroidToDictonary:
    def __init__(self, dictionary=Dictionary()):
        self.dictionary = dictionary

    def format(self, xml, language):
        root = self._get_root_element(xml)

        for child in root:
            if child.tag == 'string':
                key = child.get('name')
                value = child.text
                self.dictionary.add_translation(key, language, value)
        return self.dictionary

    def _get_root_element(self, xml):
        if isinstance(xml, str):
            root = ET.fromstring(xml)
        else:
            root = ET.parse(xml).getroot()
        return root
