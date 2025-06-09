# -*- coding: utf-8 -*-

import encodings
from functools import lru_cache
from typing import Dict, Final, FrozenSet, Set


@lru_cache
def _encodings_aliases() -> Dict[str, str]:
    return encodings.aliases.aliases


def _create_encodings() -> Set[str]:
    keys = list(_encodings_aliases().keys())
    values = list(_encodings_aliases().values())
    return set(keys + values)


ENCODINGS: Final[FrozenSet[str]] = frozenset(_create_encodings())


if __name__ == "__main__":
    for encoding in sorted(ENCODINGS):
        print(encoding)
