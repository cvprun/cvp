# -*- coding: utf-8 -*-

from re import Pattern
from re import compile as re_compile
from typing import Final, Optional, Sequence, Set, Union

RENAME_SUFFIX_PATTERN: Final[Pattern[str]] = re_compile(r"^(.*) \((\d+)\)$")


def _new_naming(prefix: str, index: int) -> str:
    return f"{prefix} ({index})"


def new_name(name: str, names: Optional[Union[Sequence[str], Set[str]]] = None) -> str:
    if not names:
        return name

    if isinstance(names, set):
        unique_names = names
    else:
        unique_names = set(names)

    if name in unique_names:
        if match_group := RENAME_SUFFIX_PATTERN.match(name):
            prefix = match_group.group(1)
            index = int(match_group.group(2))
            return new_name(_new_naming(prefix, index + 1), names)
        else:
            return new_name(_new_naming(name, 1), names)
    else:
        return name
