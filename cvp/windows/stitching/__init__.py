# -*- coding: utf-8 -*-

from cvp.config.sections.stitching import StitchingAuiConfig
from cvp.imgui.canvas import canvas_context
from cvp.imgui.draw_list.types import DrawList
from cvp.renderer.context import RendererContext
from cvp.types.override import override
from cvp.widgets.aui import AuiWindow


class StitchingWindow(AuiWindow[StitchingAuiConfig]):
    def __init__(self, context: RendererContext):
        super().__init__(
            context=context,
            window_config=context.config.stitching_aui,
            title="Stitching",
            closable=True,
        )
        self._clear_color = 0.5, 0.5, 0.5, 1.0

    @override
    def on_process_main(self) -> None:
        with canvas_context(
            "Canvas",
            clear_color=self._clear_color,
            rect_filled=True,
        ) as draw_list:
            self.on_canvas(draw_list)

    def on_canvas(self, draw_list: DrawList):
        pass
