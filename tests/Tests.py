import stringify
import unittest

from loaders.AndroidStringsLoader import AndroidStringsLoader
from loaders.IosStringsLoader import IOSStringsLoader
from model.Models import Dictionary
from utils import cell_decorator


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


class AndroidStringsLoaderTests(unittest.TestCase):
    paths_with_languages = list()
    paths_with_languages.append(('/resources/values-pl/strings.xml', 'pl'))
    paths_with_languages.append(('/resources/values-en/strings.xml', 'en'))
    paths_with_languages.append(('/resources/test/temp_dir/values-en/strings.xml', 'en'))
    paths_with_languages.append(('values-en/strings.xml', 'en'))
    paths_with_languages.append(('resources/values/strings.xml', 'en'))

    def test_decode_file_path_language(self):
        android_strings_loader = AndroidStringsLoader("/")
        for case in self.paths_with_languages:
            path = case[0]
            language = case[1]
            self.assertEqual(language, android_strings_loader._decode_filepath_language(path))


class IOSStringsLoaderTests(unittest.TestCase):
    paths_with_languages = list()
    paths_with_languages.append(('/resources/pl.lproj/Localizable.strings', 'pl'))
    paths_with_languages.append(('/resources/en.lproj/Localizable.strings', 'en'))

    def test_decode_file_path_language(self):
        ios_strings_loader = IOSStringsLoader("/")
        for case in self.paths_with_languages:
            path = case[0]
            language = case[1]
            self.assertEqual(language, ios_strings_loader._decode_filepath_language(path))


class EntryDecoratorTests(unittest.TestCase):
    bold_example = "testing<b>123</b>"
    italic_example = "testing<i>123</i>"
    mixed_example = "<b><i>TEST</i></b>"

    def test_encoding(self):
        self.assertEqual("testing[[b]]123[[/b]]", cell_decorator.encode(self.bold_example))
        self.assertEqual("testing[[i]]123[[/i]]", cell_decorator.encode(self.italic_example))
        self.assertEqual("[[b]][[i]]TEST[[/i]][[/b]]", cell_decorator.encode(self.mixed_example))


if __name__ == '__main__':
    unittest.main()
