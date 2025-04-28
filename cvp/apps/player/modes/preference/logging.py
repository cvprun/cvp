# -*- coding: utf-8 -*-

import os

from imgui_bundle import imgui

from cvp.apps.player.modes.preference._base import BasePreference
from cvp.context.context import Context
from cvp.imgui.flags.input_text import ENTER_RETURNS_TRUE
from cvp.imgui.input_text import input_text
from cvp.imgui.popups.open_file import OpenFilePopup
from cvp.logging.logging import (
    SEVERITIES,
    convert_level_number,
    loads_logging_config,
    logger,
    set_root_level,
)
from cvp.types.override import override
from cvp.variables import NOT_FOUND_INDEX


class LoggingPreference(BasePreference):
    __cvp_menu_name__ = "Logging"

    def __init__(self, context: Context):
        super().__init__(context)
        self._severities = list(SEVERITIES)
        self._logging_browser = OpenFilePopup(
            title="Select logging config file",
            target=self.on_logging_file,
        )

    @property
    def config(self):
        return self.context.config.logging

    @property
    def logging_config_path(self) -> str:
        return self.config.config_path if self.config.config_path else str()

    @logging_config_path.setter
    def logging_config_path(self, value: str):
        self.config.config_path = value

    @property
    def root_severity(self) -> str:
        return self.config.root_severity if self.config.root_severity else str()

    @root_severity.setter
    def root_severity(self, value: str):
        self.config.root_severity = value

    @property
    def severity_index(self) -> int:
        try:
            return self._severities.index(self.root_severity)
        except ValueError:
            return NOT_FOUND_INDEX

    def on_logging_file(self, file: str) -> None:
        self.logging_config_path = file

    @override
    def do_process(self) -> None:
        severity_result = imgui.combo(
            "Root Severity",
            self.severity_index,
            self._severities,
        )

        severity_changed = severity_result[0]
        severity_index = severity_result[1]
        assert isinstance(severity_index, int)

        if severity_changed and 0 <= severity_index < len(self._severities):
            severity_value = self._severities[severity_index]
            level = convert_level_number(severity_value)
            set_root_level(level)
            logger.log(level, f"Changed root severity: {severity_value}")
            self.root_severity = severity_value

        logging_path_result = input_text(
            "Logging config file",
            self.logging_config_path,
            ENTER_RETURNS_TRUE,
        )

        logging_path_changed = logging_path_result.changed
        logging_path_value = logging_path_result.value
        assert isinstance(logging_path_value, str)

        if logging_path_changed and os.path.isfile(logging_path_value):
            loads_logging_config(logging_path_value)
            logger.info(f"Loads the logging config file: '{logging_path_value}'")
            self.logging_config_path = logging_path_value

        if imgui.button("Browse"):
            if os.path.isfile(self.logging_config_path):
                self._logging_browser.set_location(self.logging_config_path)
            self._logging_browser.show()

    @override
    def do_postprocess(self) -> None:
        self._logging_browser.do_process()
