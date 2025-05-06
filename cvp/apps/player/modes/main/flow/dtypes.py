# -*- coding: utf-8 -*-

from imgui_bundle import imgui

from cvp.apps.player.modes.main._base import BaseWindow
from cvp.apps.player.widgets.flows.selectable_dtype import selectable_dtype
from cvp.context.context import Context
from cvp.imgui.begin import begin_context
from cvp.imgui.push_item_width import align_right_side_context
from cvp.types.override import override


class DtypesFlowWindow(BaseWindow):
    __cvp_window_name__ = "Dtypes"

    def __init__(self, context: Context):
        super().__init__(context)
        self._filter = str()

    @override
    def do_process(self) -> None:
        with begin_context(self.get_window_name()):
            self.do_child_process()

    def do_child_process(self) -> None:
        with align_right_side_context():
            filter_result = imgui.input_text_with_hint(
                "###Filter",
                "Filter dtypes ...",
                self._filter,
            )
            self._filter = filter_result[1]

        for dtype in self._context.flows.dtypes.values():
            if self._filter and dtype.path.find(self._filter) == -1:
                continue

            selectable_dtype(dtype, use_drag_source=True)
