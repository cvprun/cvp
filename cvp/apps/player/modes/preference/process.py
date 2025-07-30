# -*- coding: utf-8 -*-

from cvp.apps.player.modes.preference._base import BasePreference
from cvp.context.context import Context
from cvp.imgui.input_float import input_float
from cvp.types.override import override


class ProcessPreference(BasePreference):
    __cvp_menu_name__ = "Process"

    def __init__(self, context: Context):
        super().__init__(context)

    @property
    def config(self):
        return self.context.config.process

    @override
    def on_process(self) -> None:
        if interval := input_float("Update interval", self.config.update_interval):
            self.config.update_interval = interval.state

        if timeout := input_float("Teardown timeout", self.config.teardown_timeout):
            self.config.teardown_timeout = timeout.state
