from collections import namedtuple

HEADERS = {
    "User-Agent": "Mozilla/5.0",
    "Content-Type": "application/json; charset=UTF-8",
}

WordUsageExample = namedtuple("WordUsageExample", ("source_text", "target_text"))
Translation = namedtuple("Translation", ("source_word", "translation"))
