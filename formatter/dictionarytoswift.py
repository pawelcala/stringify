import io
import re


class DictionaryToSwift:
    def __init__(self, dictionary):
        self.dictionary = dictionary

    def format(self, language):
        output = io.StringIO()
        for key in self.dictionary.keys():
            value = self.dictionary.get_translation(key, language)
            output.write('"{}" = "{}";\n'.format(key, value))
        string = output.getvalue()
        output.close()
        return string


class SwiftToDictionary:
    def __init__(self, dictionary):
        self.dictionary = dictionary

    def format(self, file, language):
        for line in file:
            match = re.match(r'"(.*)".*=.*"(.*)";', line)
            if match:
                self.dictionary.add_translation(match.group(1), language, match.group(2))
        return self.dictionary
