import stringify
import unittest


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
        dictionary = stringify.Dictionary()
        dictionary.add_translation(self.key_welcome, self.lang_pl, self.pl_hello)
        self.assertEqual(self.pl_hello, dictionary.get_translation(self.key_welcome, self.lang_pl))

        dictionary.add_translation(self.key_welcome, self.lang_pl, self.pl_hello_2)
        self.assertEqual(self.pl_hello_2, dictionary.get_translation(self.key_welcome, self.lang_pl))

    def test_dictionary_keys(self):
        dictionary = stringify.Dictionary()
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
        android_strings_loader = stringify.AndroidStringsLoader("/")
        for case in self.paths_with_languages:
            path = case[0]
            language = case[1]
            self.assertEqual(language, android_strings_loader._decode_filepath_language(path))


class IOSStringsLoaderTests(unittest.TestCase):
    paths_with_languages = list()
    paths_with_languages.append(('/resources/pl.lproj/Localizable.strings', 'pl'))
    paths_with_languages.append(('/resources/en.lproj/Localizable.strings', 'en'))

    def test_decode_file_path_language(self):
        ios_strings_loader = stringify.IOSStringsLoader("/")
        for case in self.paths_with_languages:
            path = case[0]
            language = case[1]
            self.assertEqual(language, ios_strings_loader._decode_filepath_language(path))


if __name__ == '__main__':
    unittest.main()
