# -*- coding: utf-8 -*-

from inspect import getmembers, isroutine
from typing import Any, Iterable, List, Mapping, Tuple


def is_dunder(name: str) -> bool:
    """Double underscore"""
    return name.startswith("__") and name.endswith("__")


def is_sunder(name: str) -> bool:
    """Single underscore"""
    return not is_dunder(name) and name.startswith("_") and name.endswith("_")


def is_private_member(name: str) -> bool:
    return name.startswith("_")


def is_public_member(name: str) -> bool:
    return not is_private_member(name)


def is_property(obj: Any, key: str) -> bool:
    cls = obj if isinstance(obj, type) else type(obj)
    return hasattr(cls, key) and isinstance(getattr(cls, key), property)


def is_instance_public_member(obj: Any, key: str) -> bool:
    return is_public_member(key) and not is_property(obj, key)


def get_public_instance_attributes(data: Any) -> List[Tuple[str, Any]]:
    if isinstance(data, Mapping):
        return [(str(k), v) for k, v in data.items()]
    if isinstance(data, Iterable):
        return [(str(i), v) for i, v in enumerate(data)]
    attributes = getmembers(data, lambda a: not isroutine(a))
    return list(filter(lambda x: is_instance_public_member(data, x[0]), attributes))


def get_attribute_keys(obj: Any) -> List[str]:
    result = list()
    for key in dir(obj):
        if is_dunder(key):
            continue
        if is_property(obj, key):
            continue
        if isroutine(getattr(obj, key)):
            continue
        result.append(key)
    return result
