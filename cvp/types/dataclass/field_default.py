# -*- coding: utf-8 -*-

from dataclasses import MISSING, fields, is_dataclass
from typing import Type, TypeVar, Union

from cvp.types.dataclass.field_name import _T

_Key = TypeVar("_Key")


def get_field_default(cls: Union[_T, Type[_T]], key: _Key) -> _Key:
    """
    Obtain the default value of a dataclass field.

    Example:
        >>> from dataclasses import dataclass
        >>> from cvp.types.dataclass.field_name import get_field_name
        >>> @dataclass
        ... class User:
        ...     name: str = "man"
        ...     age: int = 10
        >>> name = get_field_default(User, get_field_name(User).name)
        >>> age = get_field_default(User, get_field_name(User).age)
        >>> print(name)  # "man"
        >>> print(age)   # 10
    """

    if not is_dataclass(cls):
        raise TypeError("Only classes or instances of dataclass are allowed")

    fs = fields(cls)
    f = {f.name: f for f in fs}[str(key)]

    if f.default is MISSING and f.default_factory is MISSING:
        raise ValueError(f"No default value is assigned to the field '{key}'")
    elif f.default is not MISSING and f.default_factory is MISSING:
        return f.default
    elif f.default is MISSING and f.default_factory is not MISSING:
        return f.default_factory()
    else:
        assert False, "Cannot specify both `default` and `default_factory`"
