# -*- coding: utf-8 -*-

from unicodedata import normalize as unicodedata_normalize


def normalize_nfc(unicode_text: str) -> str:
    return unicodedata_normalize("NFC", unicode_text)


def normalize_nfd(unicode_text: str) -> str:
    return unicodedata_normalize("NFD", unicode_text)


# noinspection SpellCheckingInspection
def normalize_nfkc(unicode_text: str) -> str:
    return unicodedata_normalize("NFKC", unicode_text)


# noinspection SpellCheckingInspection
def normalize_nfkd(unicode_text: str) -> str:
    return unicodedata_normalize("NFKD", unicode_text)
