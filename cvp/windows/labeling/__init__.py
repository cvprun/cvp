# -*- coding: utf-8 -*-

from cvp.config.sections.labeling import LabelingAuiConfig
from cvp.imgui.canvas import canvas_context
from cvp.renderer.context import RendererContext
from cvp.types.override import override
from cvp.widgets.aui import AuiWindow


class LabelingWindow(AuiWindow[LabelingAuiConfig]):
    def __init__(self, context: RendererContext):
        super().__init__(
            context=context,
            window_config=context.config.labeling_aui,
            title="Labeling",
            closable=True,
        )

    @override
    def on_process_main(self) -> None:
        with canvas_context():
            pass
