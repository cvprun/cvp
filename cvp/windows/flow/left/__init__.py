# -*- coding: utf-8 -*-

from cvp.imgui.fonts.mapper import FontMapper
from cvp.renderer.context import RendererContext
from cvp.widgets.tab import TabBar
from cvp.windows.flow.canvases import Canvases
from cvp.windows.flow.left.graphs import GraphsTab
from cvp.windows.flow.left.tree import TreeTab


class FlowLeftTabs(TabBar[Canvases]):
    def __init__(self, context: RendererContext, fonts: FontMapper):
        super().__init__(
            context=context,
            identifier="## FlowLeftTabs",
            flags=0,
        )
        self.register(TreeTab(context, fonts))
        self.register(GraphsTab(context, fonts))
