import stringify
import unittest

from importers.androidimporter import AndroidImporter
from importers.swiftimporter import SwiftImporter
from model.Models import Dictionary


class DictionaryTests(unittest.TestCase):
    pl_hello = 'witaj'
    pl_hello_2 = 'cześć'

    pl_bye = 'pa'
    en_bye = 'bye'

    key_welcome = 'welcome'
    key_bye = 'hello'

    lang_pl = 'pl'
    lang_en = 'en'

    def test_values_insertion(self):
        dictionary = Dictionary()
        dictionary.add_translation(self.key_welcome, self.lang_pl, self.pl_hello)
        self.assertEqual(self.pl_hello, dictionary.get_translation(self.key_welcome, self.lang_pl))

        dictionary.add_translation(self.key_welcome, self.lang_pl, self.pl_hello_2)
        self.assertEqual(self.pl_hello_2, dictionary.get_translation(self.key_welcome, self.lang_pl))

    def test_dictionary_keys(self):
        dictionary = Dictionary()
        dictionary.add_translation(self.key_welcome, self.lang_pl, self.pl_hello)
        dictionary.add_translation(self.key_bye, self.lang_pl, self.pl_bye)

        self.assertEqual(2, len(dictionary.keys()))
        self.assertEqual(1, len(dictionary.languages))

        dictionary.add_translation(self.key_bye, self.lang_en, self.en_bye)
        self.assertEqual(2, len(dictionary.keys()))
        self.assertEqual(2, len(dictionary.languages))

    def test_add(self):
        dict1 = Dictionary()
        dict2 = Dictionary()

        dict1.add_translation('hello', 'en', 'Hello')
        dict2.add_translation('hello', 'pl', 'Czesc')

        new_dict = dict1 + dict2
        self.assertEqual(len(new_dict.languages), 2)
        self.assertEqual(len(new_dict.keys()), 1)
        self.assertEqual('Hello', new_dict.get_translation('hello', 'en'))
        self.assertEqual('Czesc', new_dict.get_translation('hello', 'pl'))


class AndroidStringsLoaderTests(unittest.TestCase):
    paths_with_languages = list()
    paths_with_languages.append(('/resources/values-pl/strings.xml', 'pl'))
    paths_with_languages.append(('/resources/values-en/strings.xml', 'en'))
    paths_with_languages.append(('/resources/test/temp_dir/values-en/strings.xml', 'en'))
    paths_with_languages.append(('values-en/strings.xml', 'en'))
    paths_with_languages.append(('resources/values/strings.xml', 'en'))

    def test_decode_file_path_language(self):
        android_strings_loader = AndroidImporter("/")
        for case in self.paths_with_languages:
            path = case[0]
            language = case[1]
            self.assertEqual(language, android_strings_loader._decode_filepath_language(path))


class IOSStringsLoaderTests(unittest.TestCase):
    paths_with_languages = list()
    paths_with_languages.append(('/resources/pl.lproj/Localizable.strings', 'pl'))
    paths_with_languages.append(('/resources/en.lproj/Localizable.strings', 'en'))

    def test_decode_file_path_language(self):
        ios_strings_loader = SwiftImporter("/")
        for case in self.paths_with_languages:
            path = case[0]
            language = case[1]
            self.assertEqual(language, ios_strings_loader._decode_filepath_language(path))


if __name__ == '__main__':
    unittest.main()
