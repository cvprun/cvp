# -*- coding: utf-8 -*-

from datetime import datetime
from typing import Final, Optional

from imgui_bundle import imgui

from cvp.apps.player.modes._base import BaseMode
from cvp.assets.fonts.mdi import CALENDAR_CLOCK
from cvp.context.context import Context
from cvp.imgui.begin_child import begin_child_context
from cvp.imgui.button import button
from cvp.imgui.checkbox import checkbox
from cvp.imgui.fit_size import FIT_SIZE
from cvp.imgui.flags.child import AUTO_RESIZE_Y, BORDERS, RESIZE_X, RESIZE_Y
from cvp.imgui.input_int import input_int
from cvp.imgui.input_text import input_text
from cvp.imgui.input_text_disabled import input_text_disabled
from cvp.imgui.popups.confirm import ConfirmPopup
from cvp.imgui.popups.containers import PopupList
from cvp.imgui.text_centered import text_centered
from cvp.imgui.tooltip import hovered_tooltip_text
from cvp.imgui.widgets.logging_multiline import LoggingMultiline
from cvp.logging.loggers import scheduler_logger as logger
from cvp.scheduler.item import JobItem, JobKey
from cvp.scheduler.validate import validate_cronexpr
from cvp.types.override import override
from cvp.variables import INFINITE


class SchedulerMode(BaseMode):
    __cvp_mode_name__ = "Scheduler"
    __cvp_mode_icon__ = CALENDAR_CLOCK

    _TOP_CHILD_FLAGS: Final[int] = RESIZE_Y
    _BOTTOM_CHILD_FLAGS: Final[int] = AUTO_RESIZE_Y

    _MENU_SPLIT_X: Final[int] = 300
    _MENU_CHILD_FLAGS: Final[int] = RESIZE_X | BORDERS

    _cronexpr_error: Optional[BaseException]

    def __init__(self, context: Context):
        super().__init__(context)

        self._stopping = False
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

        self._popups = PopupList(self._confirm_remove, self._confirm_clear)
        self._logging_widget = LoggingMultiline(logger)

        self._cronexpr_error = None

    @property
    def config(self):
        return self.context.config.scheduler

    @property
    def scheduler(self):
        return self.context.scheduler

    @property
    def selected_job(self):
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
    def on_job_scheduled(self, key: str, timestamp: datetime):
        event_name = self.on_job_scheduled.__name__
        logger.info(f"{event_name}({key=}, timestamp={timestamp.isoformat()})")

    @override
    def on_job_completed(self, key: str):
        event_name = self.on_job_completed.__name__
        logger.info(f"{event_name}({key=})")

    @override
    def on_process(self) -> None:
        with self.begin_mode_context():
            if imgui.is_window_appearing():
                if self.selected_job is not None:
                    self._cronexpr_error = validate_cronexpr(self.selected_job.cron)

            half_height = imgui.get_content_region_avail().y / 2
            with begin_child_context(
                label="Top",
                size=(0, half_height),
                child_flags=self._TOP_CHILD_FLAGS,
            ):
                self.do_top_process()

            imgui.separator()

            with begin_child_context(
                label="Bottom",
                child_flags=self._BOTTOM_CHILD_FLAGS,
            ):
                self.do_bottom_toolbar_process()

            self._logging_widget.options = self.config
            self._logging_widget.do_process(use_mouse_wheel=True)

        self._popups.do_process()

    def do_top_process(self) -> None:
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

    def do_job_process(self, item: JobItem) -> None:
        input_text_disabled("UUID", item.uuid)
        is_scheduled = self.scheduler.is_scheduled(item.key)

        if item.managed:
            self.text_warning("This event is system-managed and cannot be modified")

        imgui.begin_disabled(is_scheduled or item.managed)
        try:
            item.name = input_text("Name", item.name).value

            if cronexpr := input_text("Cron expression", item.cron):
                item.cron = cronexpr.value
                self._cronexpr_error = validate_cronexpr(item.cron)

            if self._cronexpr_error is not None:
                self.text_error(str(self._cronexpr_error))
            else:
                self.text_success("Validate cronexpr")

            if enabled := checkbox("Enabled", item.enabled):
                item.enabled = enabled.state
            hovered_tooltip_text("Automatically starts when the program launches")

            if repeat := input_int("Repeat", item.repeat):
                if repeat.value == INFINITE or 0 <= repeat.value:
                    item.repeat = repeat.value

            if button("Infinite repetition"):
                item.set_infinite()
        finally:
            imgui.end_disabled()

        has_error = self._cronexpr_error is not None
        schedule_disabled = is_scheduled or item.managed or not item.cron or has_error
        unschedule_disabled = not is_scheduled or item.managed

        if button("Schedule", disabled=schedule_disabled):
            self.scheduler.schedule(item.key)
        imgui.same_line()
        if button("Unschedule", disabled=unschedule_disabled):
            self.scheduler.unschedule(item.key)

    def do_bottom_toolbar_process(self) -> None:
        running = self.scheduler.is_alive()
        if not running:
            self._stopping = False

        if self._stopping:
            button("Start", disabled=True)
            imgui.same_line()
            button("Stop", disabled=True)
        else:
            if button("Start", disabled=running):
                self.scheduler.start_safe()
            imgui.same_line()
            if button("Stop", disabled=not running):
                self.scheduler.stop()
                self._stopping = True

        imgui.same_line()

        if self._stopping:
            self.text_warning("Stopping scheduler ...")
        elif running:
            self.text_success("Scheduler is running ...")
        else:
            self.text_error("Scheduler is idle")
