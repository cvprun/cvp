# -*- coding: utf-8 -*-

from typing import Final
from unicodedata import normalize as unicodedata_normalize

NFC: Final[str] = "NFC"
NFD: Final[str] = "NFD"

# noinspection SpellCheckingInspection
NFKC: Final[str] = "NFKC"

# noinspection SpellCheckingInspection
NFKD: Final[str] = "NFKD"


def normalize_nfc(unicode_text: str) -> str:
    return unicodedata_normalize(NFC, unicode_text)


def normalize_nfd(unicode_text: str) -> str:
    return unicodedata_normalize(NFD, unicode_text)


# noinspection SpellCheckingInspection
def normalize_nfkc(unicode_text: str) -> str:
    return unicodedata_normalize(NFKC, unicode_text)


# noinspection SpellCheckingInspection
def normalize_nfkd(unicode_text: str) -> str:
    return unicodedata_normalize(NFKD, unicode_text)
