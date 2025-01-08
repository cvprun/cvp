# -*- coding: utf-8 -*-

from copy import copy, deepcopy
from dataclasses import fields, is_dataclass
from typing import Any, Dict, Optional


def public_copy(cls):
    assert is_dataclass(cls)

    def __copy__(instance):
        result = cls.__new__(cls)
        for f in fields(instance):
            if f.name.startswith("_"):
                continue
            setattr(result, f.name, copy(getattr(cls, f.name)))
        return result

    cls.__copy__ = __copy__
    return cls


def public_deepcopy(cls):
    assert is_dataclass(cls)

    def __deepcopy__(instance, memo: Optional[Dict[int, Any]] = None):
        if memo is None:
            memo = dict()
        result = cls.__new__(cls)
        for f in fields(instance):
            if f.name.startswith("_"):
                continue
            setattr(result, f.name, deepcopy(getattr(cls, f.name), memo))
        memo[id(instance)] = result
        return result

    cls.__deepcopy__ = __deepcopy__
    return cls
