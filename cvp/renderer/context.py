# -*- coding: utf-8 -*-

from os import PathLike
from typing import Union

from cvp.context.context import Context


class RendererContext(Context):
    def __init__(self, home: Union[str, PathLike[str]], *, with_init=False):
        super().__init__(home)
        if with_init:
            self._initialize()

    def _initialize(self):
        # [IMPORTANT] Avoid 'circular import' issues
        from cvp.renderer.window.mapper import WindowMapper

        self.windows = WindowMapper()
