import html
import re


def encode(entry):
    return re.sub(r"<([a-zA-Z/]*)>", r"[[\1]]", entry)


def decode(entry):
    entry_with_tags = re.sub(r"\[\[([a-zA-Z/]*)\]\]", r"<\1>", entry)
    return entry_with_tags

