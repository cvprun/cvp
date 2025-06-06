# -*- coding: utf-8 -*-

from keyword import iskeyword
from re import Pattern
from re import compile as re_compile
from typing import Final

from cvp.unicode.normalize import normalize_nfkd


def _remove_none_ascii_chars(text: str) -> str:
    result = str()
    for char in text:
        if char.isalnum():
            result += char
        else:
            result += "_"
    return result


_COLLAPSE_UNDERSCORES_REGEX: Final[Pattern[str]] = re_compile(r"_+")


def _collapse_underscores(text: str) -> str:
    return _COLLAPSE_UNDERSCORES_REGEX.sub("_", text)


def _strip_underscores(text: str) -> str:
    return text.strip("_")


def _escape_numeric_prefix(text: str) -> str:
    if text and text[0].isdigit():
        return "_" + text
    else:
        return text


def _resolve_keyword_collision(text: str) -> str:
    if iskeyword(text):
        # https://peps.python.org/pep-0008/#descriptive-naming-styles
        # single_trailing_underscore_:
        # used by convention to avoid conflicts with Python keyword
        return text + "_"
    else:
        return text


def python_symbol_case(name: str) -> str:
    text = normalize_nfkd(name)
    text = _remove_none_ascii_chars(text)
    text = _collapse_underscores(text)
    text = _strip_underscores(text)
    text = _escape_numeric_prefix(text)
    text = _resolve_keyword_collision(text)
    return text
