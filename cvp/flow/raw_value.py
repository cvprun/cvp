# -*- coding: utf-8 -*-

import pickle
from typing import Any, Union


def dumps(value: Any) -> Union[None, bool, int, float, str, bytes]:
    if value is None:
        return None
    elif isinstance(value, (bool, int, float, str)):
        return value
    else:
        return pickle.dumps(value)


def loads(value: Any) -> Any:
    if value is None:
        return None
    elif isinstance(value, (bool, int, float, str)):
        return value
    elif isinstance(value, bytes):
        return pickle.loads(value)
    else:
        raise TypeError(f"Unexpected value type: {type(value).__name__}")
