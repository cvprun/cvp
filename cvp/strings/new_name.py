# -*- coding: utf-8 -*-

from re import Pattern
from re import compile as re_compile
from typing import Final, Optional, Sequence, Set, Tuple, Union

RENAME_SUFFIX_PATTERN: Final[Pattern[str]] = re_compile(r"^(.*) \((\d+)\)$")


def append_suffix_index(prefix: str, index: int) -> str:
    return f"{prefix} ({index})"


def split_prefix_and_index(name: str) -> Tuple[str, int]:
    match = RENAME_SUFFIX_PATTERN.match(name)
    if match is None:
        raise ValueError(f"Partitioning failed: '{name}'")
    prefix = match.group(1)
    index = int(match.group(2))
    return prefix, index


def new_name(
    name: str,
    names: Optional[Union[Sequence[str], Set[str]]] = None,
    *,
    first=1,
    step=1,
) -> str:
    if not names:
        return name

    if isinstance(names, set):
        unique_names = names
    else:
        unique_names = set(names)

    if name in unique_names:
        try:
            prefix, index = split_prefix_and_index(name)
        except ValueError:
            return new_name(append_suffix_index(name, first), names)
        else:
            return new_name(append_suffix_index(prefix, index + step), names)
    else:
        return name
