# -*- coding: utf-8 -*-

from typing import Mapping

from imgui_bundle import imgui

from cvp.config.sections.dtype import DtypeManagerConfig
from cvp.dtypes.dtype import Dtype
from cvp.imgui.input_text_disabled import input_text_disabled
from cvp.renderer.context import RendererContext
from cvp.types.override import override
from cvp.widgets.manager import Manager


class DtypeManager(Manager[DtypeManagerConfig, Dtype]):
    def __init__(self, context: RendererContext):
        super().__init__(
            context=context,
            window_config=context.config.dtype_manager,
            title="Dtype Manager",
            closable=True,
            flags=None,
        )

    @override
    def get_menus(self) -> Mapping[str, Dtype]:
        return {key: value for key, value in self.context.fm.dtypes.items()}

    @override
    def on_process_sidebar_top(self) -> None:
        pass

    @override
    def on_menu(self, key: str, item: Dtype) -> None:
        imgui.text("Dtype information")
        imgui.separator()

        input_text_disabled("Name", item.class_name)
        input_text_disabled("Path", item.path)

        # item.docs
        # item.base
        # item.icon
        # item.color
