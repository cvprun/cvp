# -*- coding: utf-8 -*-

from cvp.apps.player.modes.flow._base import BaseFlowWindow
from cvp.context.context import Context
from cvp.types.override import override


class GraphFlowWindow(BaseFlowWindow):
    __cvp_flow_window_name__ = "Graph"

    def __init__(self, context: Context):
        super().__init__(context)

    @override
    def do_process(self) -> None:
        pass
