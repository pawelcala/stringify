import unittest

from formatter.android_formatters import DictionaryToAndroid, AndroidToDictionary
from formatter.ios_swift_formatters import DictionaryToSwift, SwiftToDictionary
from model.Models import Dictionary


class TestAndroidFormatter(unittest.TestCase):
    def setUp(self):
        self.dictionary = Dictionary()
        self.dictionary.add_translation('hello', 'en', 'Hi')
        self.dictionary.add_translation('welcome', 'en', 'Welcome')

    def _generate_result(self, elements=()):
        result = "<resources>"
        for element in elements:
            result += '<string name="%s">%s</string>' % element
        result += "</resources>"
        return result

    def test_template(self):
        formatter = DictionaryToAndroid(dictionary=self.dictionary, use_pretty_xml=False)
        formatted_string = formatter.format('en')
        dictionary_result = self._generate_result((('hello', 'Hi'), ('welcome', 'Welcome')))
        self.assertEqual(formatted_string, dictionary_result)

    def test_empty(self):
        self.dictionary.clear()
        formatter = DictionaryToAndroid(dictionary=self.dictionary, use_pretty_xml=False)
        result = formatter.format('en')
        expected_result = self._generate_result()
        self.assertEqual(result, expected_result)


class TestSwiftFormatter(unittest.TestCase):
    def setUp(self):
        self.dictionary = Dictionary()
        self.dictionary.add_translation('hello', 'en', 'Hi')
        self.dictionary.add_translation('welcome', 'en', 'Welcome')
        self.dictionary_result = '''"hello" = "Hi";\n"welcome" = "Welcome";\n'''

    def test_template(self):
        formatter = DictionaryToSwift(self.dictionary)
        formatted_string = formatter.format('en')
        self.assertEqual(formatted_string, self.dictionary_result)

    def test_empty(self):
        self.dictionary.clear()
        formatter = DictionaryToSwift(self.dictionary)
        formatted_string = formatter.format('en')
        self.assertTrue(len(formatted_string) == 0)


class TestAndroidToDictionary(unittest.TestCase):
    def setUp(self):
        self.xml = '''<resources>''' \
                   '''<string name="hi" formatted="false">Hi</string>''' \
                   '''<string name="welcome">Welcome</string>''' \
                   '''</resources>'''

    def test_simple(self):
        dictionary = Dictionary()
        formatter = AndroidToDictionary(dictionary)
        formatter.format(self.xml, 'en')
        self.assertEqual(dictionary.get_translation('hi', 'en'), 'Hi')
        self.assertEqual(dictionary.get_translation('welcome', 'en'), 'Welcome')
        self.assertEqual(len(dictionary.languages), 1)


class SwiftToDictionaryTests(unittest.TestCase):
    def setUp(self):
        self.localizable_content = ('"hi" = "Hi";', '"welcome"="Welcome";')

    def test_simple(self):
        dictionary = Dictionary()
        formatter = SwiftToDictionary(dictionary)
        formatter.format(self.localizable_content, 'en')

        self.assertEqual(dictionary.get_translation('hi', 'en'), 'Hi')
        self.assertEqual(dictionary.get_translation('welcome', 'en'), 'Welcome')
        self.assertEqual(len(dictionary.languages), 1)
