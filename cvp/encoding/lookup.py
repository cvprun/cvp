# -*- coding: utf-8 -*-

import encodings
from functools import lru_cache
from typing import Final, Mapping

from cvp.containers.immutable_list import ImmutableList

_DEFAULT_TEST_TEXT: Final[str] = "Hello, World"


@lru_cache
def _encodings_aliases() -> Mapping[str, str]:
    return encodings.aliases.aliases


@lru_cache
def _create_encodings() -> ImmutableList[str]:
    keys = list(_encodings_aliases().keys())
    values = list(_encodings_aliases().values())
    merged = list(set(keys + values))
    merged.sort()
    return ImmutableList(merged)


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


@lru_cache
def _create_text_encodings() -> ImmutableList[str]:
    items = list(filter(_is_text_encoding, _create_encodings()))
    items.sort()
    return ImmutableList(items)


@lru_cache
def _create_binary_encodings() -> ImmutableList[str]:
    items = list(filter(_is_binary_encoding, _create_encodings()))
    items.sort()
    return ImmutableList(items)


ENCODINGS: Final[ImmutableList[str]] = _create_encodings()
TEXT_ENCODINGS: Final[ImmutableList[str]] = _create_text_encodings()
BINARY_ENCODINGS: Final[ImmutableList[str]] = _create_binary_encodings()


if __name__ == "__main__":
    for encoding in sorted(ENCODINGS):
        print(encoding)
