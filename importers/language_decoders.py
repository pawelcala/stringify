import re


def decode_language_path_android(filepath, default_language):
    match = re.match(r'.*values([-a-z]{0,3})', filepath)
    if match:
        postfix = match.group(1)
        if len(postfix) == 3:
            postfix = postfix[-2:]
        else:
            postfix = default_language
        return postfix
    return None


def decode_language_path_swift(filepath):
    match = re.match(r'(.*)\.lproj', filepath)
    if match:
        prefix = match.group(1)
        if len(prefix) > 2:
            prefix = prefix[-2:]
        return prefix
    return None
