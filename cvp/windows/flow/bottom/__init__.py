# -*- coding: utf-8 -*-

from cvp.imgui.fonts.mapper import FontMapper
from cvp.renderer.context import RendererContext
from cvp.widgets.tab import TabBar
from cvp.windows.flow.bottom.logs import LogsTab
from cvp.windows.flow.bottom.run import RunTab
from cvp.windows.flow.canvases import Canvases


class FlowBottomTabs(TabBar[Canvases]):
    def __init__(self, context: RendererContext, fonts: FontMapper):
        super().__init__(
            context=context,
            identifier="## FlowBottomTabs",
            flags=0,
        )
        self.register(LogsTab(context, fonts))
        self.register(RunTab(context, fonts))
