# -*- coding: utf-8 -*-

from typing import Final

from imgui_bundle import imgui

from cvp.apps.player.modes._base import BaseMode
from cvp.assets.fonts.mdi import CALENDAR_CLOCK
from cvp.context.context import Context
from cvp.imgui.begin_child import begin_child_context
from cvp.imgui.button import button
from cvp.imgui.fit_size import FIT_SIZE
from cvp.imgui.flags.child import BORDERS, RESIZE_X
from cvp.imgui.input_text import input_text
from cvp.imgui.input_text_disabled import input_text_disabled
from cvp.imgui.popups.confirm import ConfirmPopup
from cvp.imgui.popups.containers import PopupList
from cvp.imgui.text_centered import text_centered
from cvp.scheduler.item import JobItem, JobKey
from cvp.types.override import override


class SchedulerMode(BaseMode):
    __cvp_mode_name__ = "Scheduler"
    __cvp_mode_icon__ = CALENDAR_CLOCK

    _MENU_SPLIT_X: Final[int] = 300
    _MENU_CHILD_FLAGS: Final[int] = RESIZE_X | BORDERS

    def __init__(self, context: Context):
        super().__init__(context)

        self._remove_candidate = str()
        self._confirm_remove = ConfirmPopup(
            title="Remove",
            label="Are you sure you want to remove schedule?",
            ok="Remove",
            cancel="No",
            target=self.on_confirm_remove,
        )
        self._confirm_clear = ConfirmPopup(
            title="Clear",
            label="Are you sure you want to remove all schedule?",
            ok="Clear",
            cancel="No",
            target=self.on_confirm_clear,
        )

        self._popups = PopupList(
            self._confirm_remove,
            self._confirm_clear,
        )

    @property
    def scheduler(self):
        return self.context.scheduler

    @property
    def selected_schedule(self):
        return self.scheduler.get(JobKey(self.selected_submenu))

    def on_confirm_remove(self, value: bool) -> None:
        if not value:
            return

        assert self._remove_candidate in self.scheduler
        self.scheduler.remove(self._remove_candidate)
        self._remove_candidate = str()

    def on_confirm_clear(self, value: bool) -> None:
        if not value:
            return
        self.scheduler.remove_all()

    @override
    def on_process(self) -> None:
        with self.begin_mode_context():
            with begin_child_context(
                label="Menu",
                size=(self._MENU_SPLIT_X, 0),
                child_flags=self._MENU_CHILD_FLAGS,
            ):
                if button("Reload"):
                    self.scheduler.read_all_config_files()
                imgui.same_line()
                if button("Add"):
                    self.scheduler.add_job()
                imgui.same_line()
                is_any_selected = self.selected_submenu in self.scheduler
                if button("Del", disabled=not is_any_selected):
                    self._remove_candidate = self.selected_submenu
                    self._confirm_remove.show()
                imgui.same_line()
                if button("Clear", disabled=not self.scheduler):
                    self._confirm_clear.show()

                if imgui.begin_list_box("##List", FIT_SIZE):
                    try:
                        for key, job in self.scheduler.items():
                            label = f"{job.name}###{key}" if job.name else key
                            selected = key == self.selected_submenu
                            if imgui.selectable(label, selected)[1]:
                                self.selected_submenu = key
                    finally:
                        imgui.end_list_box()

            imgui.same_line()

            with begin_child_context("Main"):
                if item := self.scheduler.get(JobKey(self.selected_submenu)):
                    self.do_job_process(item)
                else:
                    text_centered("Please select a item")

        self._popups.do_process()

    def do_job_process(self, job: JobItem) -> None:
        input_text_disabled("UUID", job.uuid)
        job.name = input_text("Name", job.name).value

        # job.cron: str = field(default_factory=str)
        # job.enabled: bool = False
        # job.repeat: int = INFINITE
