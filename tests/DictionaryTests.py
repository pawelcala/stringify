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

if __name__ == '__main__':
    unittest.main()
