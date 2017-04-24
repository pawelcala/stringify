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
