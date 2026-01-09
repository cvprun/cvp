# -*- coding: utf-8 -*-

from cvp.context.context import Context


class CliApplication:
    def __init__(self, context: Context):
        self._context = context

    def start(self) -> None:
        pass
