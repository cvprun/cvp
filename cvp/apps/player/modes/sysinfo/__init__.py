# -*- coding: utf-8 -*-

import platform

import psutil
from imgui_bundle import imgui

from cvp.apps.player.modes._base import BaseMode
from cvp.assets.fonts.mdi import INFORMATION_VARIANT_CIRCLE
from cvp.context.context import Context
from cvp.imgui.begin_child import begin_child_context
from cvp.imgui.input_text_disabled import input_text_disabled
from cvp.maths.numeral.binary_prefixes import binary_prefix_with_integer
from cvp.types.override import override


class SysinfoMode(BaseMode):
    __cvp_mode_name__ = "Sysinfo"
    __cvp_mode_icon__ = INFORMATION_VARIANT_CIRCLE

    def __init__(self, context: Context):
        super().__init__(context)

    @override
    def on_process(self) -> None:
        with self.begin_mode_context():
            with begin_child_context("Main"):
                self.on_platform_process()
                imgui.separator()
                self.on_cpu_process()
                imgui.separator()
                self.on_memory_process()
                imgui.separator()
                self.on_root_disk_process()

    @staticmethod
    def on_platform_process() -> None:
        input_text_disabled("System", platform.system())
        input_text_disabled("Node Name", platform.node())
        input_text_disabled("Release", platform.release())
        input_text_disabled("Version", platform.version())
        input_text_disabled("Machine", platform.machine())
        input_text_disabled("Processor", platform.processor())

    @staticmethod
    def on_cpu_process() -> None:
        input_text_disabled("CPU Usage", str(psutil.cpu_percent(interval=0.1)))

    @staticmethod
    def on_memory_process() -> None:
        mem = psutil.virtual_memory()

        input_text_disabled("Memory Percent", f"{mem.percent}%")

        mem_used_scaled, mem_used_prefix = binary_prefix_with_integer(mem.used)
        mem_used = f"{mem_used_scaled}{mem_used_prefix.sym0}Byte"
        input_text_disabled("Memory Used", mem_used)

        mem_total_scaled, mem_total_prefix = binary_prefix_with_integer(mem.total)
        mem_total = f"{mem_total_scaled}{mem_total_prefix.sym0}Byte"
        input_text_disabled("Memory Used", mem_total)

    @staticmethod
    def on_root_disk_process() -> None:
        disk = psutil.disk_usage("/")

        input_text_disabled("Disk Percent", f"{disk.percent}%")

        disk_used_scaled, disk_used_prefix = binary_prefix_with_integer(disk.used)
        disk_used = f"{disk_used_scaled}{disk_used_prefix.sym0}Byte"
        input_text_disabled("Disk Used", disk_used)

        disk_total_scaled, disk_total_prefix = binary_prefix_with_integer(disk.total)
        disk_total = f"{disk_total_scaled}{disk_total_prefix.sym0}Byte"
        input_text_disabled("Disk Used", disk_total)
