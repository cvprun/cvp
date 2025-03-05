# -*- coding: utf-8 -*-

from cvp.renderer.context import RendererContext
from cvp.widgets.canvas.tabs import FlowCanvasTabs
from cvp.widgets.tab import TabBar
from cvp.windows.flow.left.tree import TreeTab


class FlowLeftTabs(TabBar[FlowCanvasTabs]):
    def __init__(self, context: RendererContext):
        super().__init__(
            context=context,
            identifier="## FlowLeftTabs",
            flags=0,
        )
        self.register(TreeTab(context))
