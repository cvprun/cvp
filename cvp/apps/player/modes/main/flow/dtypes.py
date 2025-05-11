# -*- coding: utf-8 -*-

from imgui_bundle import imgui

from cvp.apps.player.modes.main._base import BaseWindow
from cvp.apps.player.modes.main.position import DockPosition
from cvp.apps.player.widgets.flows.selectable_dtype import selectable_dtype
from cvp.context.context import Context
from cvp.dtypes.dtype import Dtype
from cvp.imgui.input_text_disabled import input_text_disabled
from cvp.imgui.push_item_width import align_right_side_context
from cvp.imgui.text_centered import text_centered
from cvp.types.override import override


class DtypeFlowWindow(BaseWindow):
    __cvp_window_name__ = "Dtype"
    __cvp_window_position__ = DockPosition.center_bottom

    def __init__(self, context: Context):
        super().__init__(context)

    @property
    def dtypes(self):
        return self.context.flows.dtypes

    @override
    def on_main_process(self) -> None:
        if dtype := self.dtypes.get(self.selected_submenu):
            self.do_dtype_process(dtype)
        else:
            text_centered("Please select a item")

    @staticmethod
    def do_dtype_process(dtype: Dtype) -> None:
        input_text_disabled("Module Path", dtype.module_path)
        input_text_disabled("Class Name", dtype.class_name)
        imgui.input_text_multiline("Docs", dtype.docs)


class DtypesFlowWindow(BaseWindow):
    __cvp_window_name__ = "Dtypes"
    __cvp_window_position__ = DockPosition.left_bottom

    def __init__(self, context: Context):
        super().__init__(context)
        self._filter = str()

    def get_selected_dtype(self, *, suffix=None) -> str:
        return self._context.get_selected_submenu(DtypeFlowWindow, suffix=suffix)

    def set_selected_dtype(self, value: str, *, suffix=None) -> None:
        self._context.set_selected_submenu(DtypeFlowWindow, value, suffix=suffix)

    @override
    def on_main_process(self) -> None:
        with align_right_side_context():
            filter_result = imgui.input_text_with_hint(
                "###Filter",
                "Filter dtypes ...",
                self._filter,
            )
            self._filter = filter_result[1]

        selected_dtype = self.get_selected_dtype()
        for dtype in self._context.flows.dtypes.values():
            if self._filter and dtype.path.find(self._filter) == -1:
                continue

            selected = dtype.path == selected_dtype
            if selectable_dtype(dtype, selected=selected, use_drag_source=True):
                self.set_selected_dtype(dtype.path)
