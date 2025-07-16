# -*- coding: utf-8 -*-

from tempfile import TemporaryDirectory

from cvp.context.context import Context


class TempContext(Context):
    def __init__(self):
        self._tempdir = TemporaryDirectory()
        super().__init__(self._tempdir.name)

    @property
    def tempdir(self):
        return self._tempdir
