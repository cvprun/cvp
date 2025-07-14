# -*- coding: utf-8 -*-

import encodings
from functools import lru_cache
from typing import Dict, Final, FrozenSet, Set

_DEFAULT_TEST_TEXT: Final[str] = "Hello, World"


@lru_cache
def _encodings_aliases() -> Dict[str, str]:
    return encodings.aliases.aliases


def _create_encodings() -> Set[str]:
    keys = list(_encodings_aliases().keys())
    values = list(_encodings_aliases().values())
    return set(keys + values)


def _is_text_encoding(encoding_name: str, test_text=_DEFAULT_TEST_TEXT) -> bool:
    try:
        test_bytes = test_text.encode(encoding="utf-8", errors="strict")

        decoded = test_bytes.decode(encoding_name)
        encoded = decoded.encode(encoding_name)

        # Checking if the original and re-encoded results are identical
        return isinstance(decoded, str) and isinstance(encoded, bytes)
    except (UnicodeDecodeError, UnicodeEncodeError, LookupError, TypeError):
        return False


def _is_binary_encoding(encoding_name: str, test_text=_DEFAULT_TEST_TEXT) -> bool:
    return not _is_text_encoding(encoding_name, test_text)


def _create_text_encodings() -> Set[str]:
    return set(filter(_is_text_encoding, _create_encodings()))


def _create_binary_encodings() -> Set[str]:
    return set(filter(_is_binary_encoding, _create_encodings()))


ENCODINGS: Final[FrozenSet[str]] = frozenset(_create_encodings())
TEXT_ENCODINGS: Final[FrozenSet[str]] = frozenset(_create_text_encodings())
BINARY_ENCODINGS: Final[FrozenSet[str]] = frozenset(_create_binary_encodings())


if __name__ == "__main__":
    for encoding in sorted(ENCODINGS):
        print(encoding)
