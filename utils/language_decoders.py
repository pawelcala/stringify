import re


class AndroidLanguagePathDecoder:
    def __init__(self, filepath, default_language):
        self.default_language = default_language
        self.filepath = filepath

    def decode(self):
        match = re.match(r'.*values([-a-z]{0,3})', self.filepath)
        if match:
            postfix = match.group(1)
            if len(postfix) == 3:
                postfix = postfix[-2:]
            else:
                postfix = self.default_language
            return postfix
        return None


class IosSwiftLanguagePathDecoder:
    def __init__(self, filepath):
        self.filepath = filepath

    def decode(self):
        match = re.match(r'(.*)\.lproj', self.filepath)
        if match:
            prefix = match.group(1)
            if len(prefix) > 2:
                prefix = prefix[-2:]
            return prefix
        return None
