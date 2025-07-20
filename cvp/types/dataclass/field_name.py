# -*- coding: utf-8 -*-

from argparse import Namespace
from dataclasses import fields, is_dataclass
from typing import Type, TypeVar, Union

_T = TypeVar("_T")


def get_field_name(cls: Union[_T, Type[_T]]) -> Type[_T]:
    """
    A tricky attempt to access the field names of a data class via IDE autocomplete.

    Normally, trying to access field names using syntax like
    `DataclassClassType.attribute_name.__name__` will raise an `AttributeError`.
    To avoid this, developers typically use string literals like "attribute_name",
    but this approach is error-prone and lacks the benefits of symbol-based
    autocomplete.

    This function works around that limitation by returning a `Namespace` object
    where each dataclass field name is both the key and the value. This allows
    symbol-based access to field names (e.g., `field_names.attribute_name`) with
    autocomplete support in modern IDEs.

    Parameters:
        cls: A dataclass instance or class.

    Returns:
        A `Namespace` object where each attribute corresponds to a dataclass field name,
        allowing safe and IDE-friendly access to field names as strings.

    Raises:
        TypeError: If the input is not a dataclass class or instance.

    Example:
        >>> from dataclasses import dataclass
        >>> @dataclass
        ... class User:
        ...     name: str
        ...     age: int
        >>> keys = get_field_name(User)
        >>> # Once you type `keys.`, autocomplete suggestions will appear in the IDE.
        >>> print(keys.name)  # "name"
        >>> print(keys.age)   # "age"
    """

    if not is_dataclass(cls):
        raise TypeError("Only classes or instances of dataclass are allowed")

    if not isinstance(cls, type):
        cls = type(cls)  # type: ignore[assignment]

    names = {f.name: f.name for f in fields(cls)}  # type: ignore[arg-type]

    # noinspection PyTypeChecker
    return Namespace(**names)  # type: ignore[return-value]
