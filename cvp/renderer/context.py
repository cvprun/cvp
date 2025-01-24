# -*- coding: utf-8 -*-

from os import PathLike
from typing import Union

from cvp.context.context import Context
from cvp.inspect.member import get_attribute_keys


class RendererContext(Context):
    def __init__(self, home: Union[str, PathLike[str]]):
        super().__init__(home)

    @classmethod
    def from_context(cls, context: Context):
        result = cls.__new__(cls)
        for key in get_attribute_keys(context):
            setattr(result, key, getattr(context, key))
        return result
