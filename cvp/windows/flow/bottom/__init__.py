# -*- coding: utf-8 -*-

from cvp.renderer.context import RendererContext
from cvp.widgets.canvas.tabs import FlowCanvasTabs
from cvp.widgets.tab import TabBar
from cvp.windows.flow.bottom.logs import LogsTab
from cvp.windows.flow.bottom.run import RunTab


class FlowBottomTabs(TabBar[FlowCanvasTabs]):
    def __init__(self, context: RendererContext):
        super().__init__(
            context=context,
            identifier="## FlowBottomTabs",
            flags=0,
        )
        self.register(LogsTab(context))
        self.register(RunTab(context))
