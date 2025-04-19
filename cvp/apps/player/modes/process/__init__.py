# -*- coding: utf-8 -*-

from collections import OrderedDict
from functools import lru_cache
from typing import Final, Sequence, Type

from imgui_bundle import imgui

from cvp.apps.player.modes._base import BaseMode
from cvp.apps.player.modes.process._base import BaseProcessTab
from cvp.context.context import Context
from cvp.imgui.begin import begin_context
from cvp.imgui.begin_child import begin_child_context
from cvp.imgui.button import button
from cvp.imgui.fit_size import FIT_SIZE
from cvp.imgui.flags.child import BORDERS, RESIZE_X
from cvp.imgui.flags.style_var import StyleVar
from cvp.imgui.flags.window import ROOT_STATIC_VIEWPORT_FLAGS
from cvp.imgui.set_next_window_as_viewport import set_next_window_as_viewport
from cvp.imgui.text_centered import text_centered
from cvp.popups.confirm import ConfirmPopup
from cvp.process.process import Process
from cvp.types.override import override

_MENU_SPLIT_X: Final[int] = 300
_MENU_CHILD_FLAGS: Final[int] = RESIZE_X | BORDERS


@lru_cache
def create_process_tab_types() -> Sequence[Type[BaseProcessTab]]:
    from cvp.apps.player.modes.process.info import ProcessInfoTab
    from cvp.apps.player.modes.process.stream import ProcessStreamTab

    return ProcessInfoTab, ProcessStreamTab


def create_process_tabs(context: Context):
    tab_types = create_process_tab_types()
    return OrderedDict({tt.get_tab_name(): tt(context) for tt in tab_types})


class ProcessMode(BaseMode):
    __cvp_mode_name__ = "Process"

    def __init__(self, context: Context):
        super().__init__(context)
        self._tabs = create_process_tabs(context)
        self._remove_candidate = str()
        self._confirm_remove = ConfirmPopup(
            title="Remove",
            label="Are you sure you want to remove process?",
            ok="Remove",
            cancel="No",
            target=self.on_confirm_remove,
        )
        self._confirm_clear = ConfirmPopup(
            title="Clear",
            label="Are you sure you want to remove all processes?",
            ok="Clear",
            cancel="No",
            target=self.on_confirm_clear,
        )

    @property
    def config(self):
        return self.context.config.process

    @property
    def processes(self):
        return self.context.pm.processes

    def on_confirm_remove(self, value: bool) -> None:
        if not value:
            return
        assert self._remove_candidate in self.processes
        self.processes.pop(self._remove_candidate)

    def on_confirm_clear(self, value: bool) -> None:
        if not value:
            return
        self.processes.clear()

    @override
    def do_process(self) -> None:
        imgui.push_style_var(StyleVar.window_border_size, 0)
        try:
            set_next_window_as_viewport()
            with begin_context(type(self).__name__, flags=ROOT_STATIC_VIEWPORT_FLAGS):
                self.do_child_process()
        finally:
            imgui.pop_style_var()

    def do_child_process(
        self,
        menu_split_x=_MENU_SPLIT_X,
        menu_child_flags=_MENU_CHILD_FLAGS,
    ) -> None:
        with begin_child_context("Menu", menu_split_x, child_flags=menu_child_flags):
            if button("Del", disabled=self.selected not in self.processes):
                self._remove_candidate = self.selected
                self._confirm_remove.show()
            imgui.same_line()
            if button("Clear", disabled=not self.processes):
                self._confirm_clear.show()

            if imgui.begin_list_box("##List", FIT_SIZE):
                try:
                    for key, process in self.processes.items():
                        label = f"{process.name}###{key}"
                        selected = key == self.selected
                        if imgui.selectable(label, selected)[1]:
                            self.selected = key
                finally:
                    imgui.end_list_box()

        imgui.same_line()

        with begin_child_context("Main"):
            if selected_process := self.processes.get(self.selected):
                self.do_process_tab_bar(selected_process)
            else:
                text_centered("Please select a item")

        self._confirm_remove.do_process()
        self._confirm_clear.do_process()

    def do_process_tab_bar(self, process: Process) -> None:
        if imgui.begin_tab_bar("Tabs"):
            try:
                for name, tab in self._tabs.items():
                    if imgui.begin_tab_item(name)[0]:
                        try:
                            tab.do_process(process)
                        finally:
                            imgui.end_tab_item()
            finally:
                imgui.end_tab_bar()
