class TranslationRow:
    def __init__(self, key):
        self.key = key
        self.translations = dict()

    def add_translation(self, lang, value):
        self.translations.update({lang: value})

    def get_translation(self, lang):
        return self.translations.get(lang)


class Dictionary:
    def __init__(self):
        self.dictionary = dict()
        self.languages = set()

    def add_translation(self, key, lang, word, comment=None):
        self.languages.add(lang)
        translation_row = self.dictionary.get(key)
        if translation_row is None:
            translation_row = TranslationRow(key)
            self.dictionary.update({translation_row.key: translation_row})

        translation_row.add_translation(lang, word)

    def get_translation(self, key, lang):
        return self.dictionary.get(key).get_translation(lang)

    def keys_iterator(self):
        return self.dictionary

    def keys(self):
        return self.dictionary.keys()

    def is_empty(self):
        return len(self.languages) == 0 or len(self.dictionary) == 0

    def clear(self):
        self.dictionary.clear()
        self.languages.clear()

    def __add__(self, other):
        new_dictionary = Dictionary()
        self._populate_dictionary(new_dictionary, self)
        self._populate_dictionary(new_dictionary, other)
        return new_dictionary

    def _populate_dictionary(self, dst_dictionary, src_dictionary):
        for lang in src_dictionary.languages:
            for key in src_dictionary.keys_iterator():
                word = src_dictionary.get_translation(key, lang)
                dst_dictionary.add_translation(key, lang, word)
