# -*- coding: utf-8 -*-

from signal import Signals
from typing import Optional

import psutil
from imgui_bundle import imgui

from cvp.apps.player.modes.services.control_cache import ServicesControlCache
from cvp.assets.fonts import mdi
from cvp.context.context import Context
from cvp.imgui.button import button
from cvp.imgui.button_signals import button_signals
from cvp.imgui.widgets.psutil.cpu_affinity_edit import cpu_affinity_edit
from cvp.imgui.widgets.psutil.ionice_edit import ionice_edit
from cvp.imgui.widgets.psutil.nice_edit import nice_edit
from cvp.imgui.widgets.psutil.rlimit_edit import rlimit_edit
from cvp.logging.loggers import logger
from cvp.process.status import ProcessStatusEx
from cvp.service.item import ServiceItem, ServiceKey


class ServicesControlTab:
    def __init__(self, context: Context):
        self._context = context
        self._signal = Signals.SIGINT
        self._cache = ServicesControlCache()

    @property
    def context(self):
        return self._context

    @property
    def services(self):
        return self.context.services

    @property
    def warning_color(self):
        return self.context.config.appearance.warning_color

    @property
    def error_color(self):
        return self.context.config.appearance.error_color

    def text_warning(self, text: str) -> None:
        imgui.text_colored(self.warning_color, text)

    def text_error(self, text: str) -> None:
        imgui.text_colored(self.error_color, text)

    def get_psutil_process(self, key: ServiceKey) -> Optional[psutil.Process]:
        process = self.services.get_process(key)
        return process.psutil if process is not None else None

    def do_remote_control_process(self, service: ServiceItem) -> None:
        name = service.name if service.name else service.uuid
        status = self.services.status(service.key)
        imgui.text(f"{name} ({status.upper()})")

        locked = service.freeze
        spawnable = self.services.spawnable(service.key)
        stoppable = self.services.stoppable(service.key)
        removable = self.services.removable(service.key)
        suspended = status in (ProcessStatusEx.stopped, ProcessStatusEx.suspended)

        if button(f"{mdi.PLAY} Spawn", disabled=not locked or not spawnable):
            assert not self.services.has_process(service.key)
            self.services.spawn(service.key)

        imgui.same_line()
        disabled_suspend = not locked or not stoppable or suspended
        if button(f"{mdi.PAUSE} Suspend", disabled=disabled_suspend):
            process = self.services.get_process(service.key)
            assert process is not None
            process.psutil.suspend()

        imgui.same_line()
        disabled_resume = not locked or not stoppable or not suspended
        if button(f"{mdi.PLAY_OUTLINE} Resume", disabled=disabled_resume):
            process = self.services.get_process(service.key)
            assert process is not None
            process.psutil.resume()

        imgui.same_line()
        disabled_interrupt = not locked or not stoppable or suspended
        if button(f"{mdi.STOP} Interrupt", disabled=disabled_interrupt):
            assert self.services.has_process(service.key)
            self.services.interrupt(service.key)

        imgui.same_line()
        disabled_kill = not locked or not stoppable
        if button(f"{mdi.ALERT} Kill", disabled=disabled_kill):
            process = self.services.get_process(service.key)
            assert process is not None
            process.psutil.kill()

        imgui.same_line()
        disabled_remove = not locked or not removable
        if button(f"{mdi.DELETE} Remove", disabled=disabled_remove):
            assert self.services.has_process(service.key)
            self.services.removable_pop(service.key)

        if not locked:
            imgui.same_line()
            self.text_error("The service cannot be controlled unless it is locked")
            return

    def __call__(self, service: ServiceItem) -> None:
        stoppable = self.services.stoppable(service.key)
        imgui.begin_disabled(not stoppable)
        try:
            if process := self.services.get_process(service.key):
                self._cache.update_if_pid_changed(process.psutil)

            if button(f"{mdi.REFRESH} Refresh"):
                self._cache.force_update(process.psutil)

            self.do_signals_process(service.key)
            self.do_nice_process(service.key)
            self.do_ionice_process(service.key)
            self.do_cpu_affinity_process(service.key)
            self.do_rlimit_process(service.key)
        finally:
            imgui.end_disabled()

    def do_signals_process(self, key: ServiceKey) -> None:
        signum = button_signals(
            label="Signals",
            top_title="Interrupt signal",
            border=True,
            debugging=self.context.debug and 2 <= self.context.verbose,
        )
        if signum is not None:
            process = self.services.get_process(key)
            assert process is not None
            process.psutil.send_signal(signum)

    def do_nice_process(self, key: ServiceKey) -> None:
        if nice_result := nice_edit(
            label="Niceness",
            nice=self._cache.nice,
            top_title="Process Niceness (Priority)",
            border=True,
        ):
            process = self.services.get_process(key)
            assert process is not None
            assert not self._cache.nice.changed

            try:
                process.psutil.nice(nice_result.value)
            except BaseException as e:
                self.context.toast_error(e, logger)
            else:
                self._cache.force_update(process.psutil)

    def do_ionice_process(self, key: ServiceKey) -> None:
        if not (psutil.LINUX or psutil.WINDOWS):  # Windows Vista+
            return

        if ionice_result := ionice_edit(
            label="IONiceness",
            ionice_class=self._cache.ionice_class,
            ionice_level=self._cache.ionice_level,
            top_title="Process I/O niceness (Priority)",
            border=True,
        ):
            process = self.services.get_process(key)
            assert process is not None
            assert not self._cache.ionice_class.changed
            assert not self._cache.ionice_level.changed

            try:
                ioclass = ionice_result.ioclass
                level = ionice_result.level
                process.psutil.ionice(ioclass, level)
            except BaseException as e:
                self.context.toast_error(e, logger)
            else:
                self._cache.force_update(process.psutil)

    def do_cpu_affinity_process(self, key: ServiceKey) -> None:
        if not (psutil.LINUX or psutil.WINDOWS or psutil.FREEBSD):
            return

        if cpu_affinity_result := cpu_affinity_edit(
            label="CPUAffinity",
            cpu_indexes=self._cache.cpu_indexes,
            cpu_affinity=self._cache.cpu_affinity,
            top_title="Process CPU Affinity",
            border=True,
        ):
            process = self.services.get_process(key)
            assert process is not None
            assert not self._cache.cpu_affinity.changed

            try:
                process.psutil.cpu_affinity(cpu_affinity_result.value)
            except BaseException as e:
                self.context.toast_error(e, logger)
            else:
                self._cache.force_update(process.psutil)

    def do_rlimit_process(self, key: ServiceKey) -> None:
        if not (psutil.LINUX or psutil.FREEBSD):
            return

        if rlimit_result := rlimit_edit(
            label="ResourceLimits",
            rlimit=self._cache.rlimit,
            top_title="Process resource limits",
            border=True,
        ):
            process = self.services.get_process(key)
            assert process is not None
            assert not self._cache.rlimit.changed

            try:
                for changed_key in rlimit_result.keys:
                    item = rlimit_result.value[changed_key]
                    process.psutil.rlimit(item.resource, item.limits)
            except BaseException as e:
                self.context.toast_error(e, logger)
            else:
                self._cache.force_update(process.psutil)
