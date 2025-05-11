# -*- coding: utf-8 -*-

from cvp.apps.player.modes.main._base import BaseWindow
from cvp.apps.player.modes.main.position import DockPosition
from cvp.context.context import Context
from cvp.types.override import override


class PropsCanvasWindow(BaseWindow):
    __cvp_window_name__ = "Props"
    __cvp_window_position__ = DockPosition.right_top

    def __init__(self, context: Context):
        super().__init__(context)

    @override
    def on_main_process(self) -> None:
        pass
