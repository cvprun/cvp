# -*- coding: utf-8 -*-

from cvp.apps.player.modes.main._base import BaseWindow
from cvp.context.context import Context


class MainWindow(BaseWindow):
    def __init__(self, context: Context):
        super().__init__(context)
