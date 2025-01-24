# -*- coding: utf-8 -*-

import os
from typing import Final, Sequence

import imgui

from cvp.logging.logging import (
    SEVERITIES,
    convert_level_number,
    loads_logging_config,
    logger,
    set_root_level,
)
from cvp.popups.open_file import OpenFilePopup
from cvp.renderer.context import RendererContext
from cvp.renderer.popup.base import PopupBase
from cvp.renderer.popup.propagator import PopupPropagator
from cvp.types.override import override
from cvp.windows.preference._base import PreferenceWidget

NOT_FOUND_INDEX: Final[int] = -1


class LoggingPreference(PopupPropagator, PreferenceWidget):
    def __init__(self, context: RendererContext, label="Logging"):
        self._config = context.config.logging
        self._label = label
        self._severities = list(SEVERITIES)
        self._logging_browser = OpenFilePopup(
            "Select logging config file",
            target=self.on_logging_file,
        )

    @property
    @override
    def label(self) -> str:
        return self._label

    @property
    @override
    def popups(self) -> Sequence[PopupBase]:
        return [self._logging_browser]

    @property
    def config_path(self) -> str:
        return self._config.config_path if self._config.config_path else str()

    @config_path.setter
    def config_path(self, value: str):
        self._config.config_path = value

    @property
    def root_severity(self) -> str:
        return self._config.root_severity if self._config.root_severity else str()

    @root_severity.setter
    def root_severity(self, value: str):
        self._config.root_severity = value

    @property
    def severity_index(self) -> int:
        try:
            return self._severities.index(self.root_severity)
        except ValueError:
            return NOT_FOUND_INDEX

    def on_logging_file(self, file: str) -> None:
        self.config_path = file

    @override
    def on_process(self) -> None:
        imgui.text("Logging config file:")
        logging_path_result = imgui.input_text(
            "##LoggingPath",
            self.config_path,
            -1,
            imgui.INPUT_TEXT_ENTER_RETURNS_TRUE,
        )

        logging_path_changed = logging_path_result[0]
        logging_path_value = logging_path_result[1]
        assert isinstance(logging_path_value, str)

        if logging_path_changed and os.path.isfile(logging_path_value):
            loads_logging_config(logging_path_value)
            logger.info(f"Loads the logging config file: '{logging_path_value}'")
            self.config_path = logging_path_value

        imgui.same_line()
        if imgui.button("Browse"):
            self._logging_browser.show()

        imgui.text("Root severity:")
        severity_result = imgui.combo(
            "##RootSeverity",
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
