# -*- coding: utf-8 -*-

from os import PathLike
from typing import Union

from cvp.context.context import Context
from cvp.inspect.member import is_dunder, is_property


class RendererContext(Context):
    def __init__(self, home: Union[str, PathLike[str]]):
        super().__init__(home)

    @staticmethod
    def get_available_context_keys(context: Context):
        result = list()
        for key in dir(context):
            if is_dunder(key):
                continue
            if is_property(context, key):
                continue
            if callable(getattr(context, key)):
                continue
            result.append(key)
        return result

    @classmethod
    def from_context(cls, context: Context):
        result = cls.__new__(cls)
        for key in cls.get_available_context_keys(context):
            setattr(result, key, getattr(context, key))
        return result
