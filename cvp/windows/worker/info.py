# -*- coding: utf-8 -*-

from cvp.config.sections.worker import WorkerConfig
from cvp.imgui.input_text_disabled import input_text_disabled
from cvp.imgui.input_text_value import input_text_value
from cvp.renderer.context import RendererContext
from cvp.types.override import override
from cvp.widgets.tab import TabItem


class WorkerInfoTab(TabItem[WorkerConfig]):
    def __init__(self, context: RendererContext):
        super().__init__(context, "Info")

    @override
    def on_item(self, item: WorkerConfig) -> None:
        input_text_disabled("UUID", item.uuid)
        item.name = input_text_value("Name", item.name)
