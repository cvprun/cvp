# -*- coding: utf-8 -*-

from cvp.imgui.fonts.mapper import FontMapper
from cvp.renderer.context import RendererContext
from cvp.widgets.tab import TabBar
from cvp.windows.flow.canvases import Canvases
from cvp.windows.flow.right.history import HistoryTab
from cvp.windows.flow.right.props import PropsTab


class FlowRightTabs(TabBar[Canvases]):
    def __init__(self, context: RendererContext, fonts: FontMapper):
        super().__init__(
            context=context,
            identifier="## FlowRightTabs",
            flags=0,
        )
        self.register(PropsTab(context, fonts))
        self.register(HistoryTab(context, fonts))
