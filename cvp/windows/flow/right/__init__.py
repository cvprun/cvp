# -*- coding: utf-8 -*-

from cvp.renderer.context import RendererContext
from cvp.widgets.canvas.tabs import FlowCanvasTabs
from cvp.widgets.tab import TabBar
from cvp.windows.flow.right.props import PropsTab


class FlowRightTabs(TabBar[FlowCanvasTabs]):
    def __init__(self, context: RendererContext):
        super().__init__(
            context=context,
            identifier="## FlowRightTabs",
            flags=0,
        )
        self.register(PropsTab(context))
