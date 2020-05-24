import re
from typing import Pattern, Optional, Dict, AnyStr, Set, Iterable

ESCAPE_REVERSE_SET = set(".")


def _reverse_escape(characters: Set[str], s: str) -> Iterable[str]:
    escaped = False
    ESC = "\\"
    for c in s:
        if escaped:
            if c not in characters:
                yield ESC
            yield c
            escaped = False
        else:
            if c == ESC:
                escaped = True
            else:
                if c in characters:
                    yield ESC
                yield c


def convert_pattern(pattern: str) -> str:
    pattern = ''.join(_reverse_escape(ESCAPE_REVERSE_SET, pattern))
    pattern = re.sub(r"([^\\]|^)\(\?(\w+):", r"\g<1>(?P<\g<2>>", pattern)
    return pattern


class UrlFriendlySearch:
    pattern: Pattern

    def __init__(self, pattern: str):
        self.pattern = re.compile(convert_pattern(pattern))

    def match(self, s: str) -> Optional[Dict[str, str]]:
        r = self.pattern.search(s)
        if r is not None:
            return r.groupdict()
        else:
            return None
