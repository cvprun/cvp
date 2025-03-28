# -*- coding: utf-8 -*-

from os import PathLike
from typing import Union

from cvp.context.context import Context
from cvp.inspect.member import get_attribute_keys


class RendererContext(Context):
    def __init__(self, home: Union[str, PathLike[str]], *, with_init=False):
        super().__init__(home)
        if with_init:
            self._initialize()

    @classmethod
    def from_context(cls, context: Context, *, with_init=False):
        result = cls.__new__(cls)
        for key in get_attribute_keys(context):
            setattr(result, key, getattr(context, key))
        if with_init:
            result._initialize()
        return result

    def _initialize(self):
        # [IMPORTANT] Avoid 'circular import' issues
        from cvp.imgui.fonts.mapper import FontMapper
        from cvp.renderer.window.mapper import WindowMapper

        self.windows = WindowMapper()
        self.fonts = FontMapper()
