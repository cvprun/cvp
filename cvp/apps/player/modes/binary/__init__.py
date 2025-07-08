# -*- coding: utf-8 -*-

import codecs
import encodings
import sys
from enum import Enum, auto, unique
from typing import Final, Optional, Union

from imgui_bundle import imgui

from cvp.apps.player.modes._base import BaseMode
from cvp.assets.fonts.mdi import HEXADECIMAL
from cvp.context.context import Context
from cvp.encoding.binary_text import (
    BinaryToText,
    binary_to_text_decoding,
    binary_to_text_encoding,
)
from cvp.encoding.lookup import ENCODINGS
from cvp.exceptions.traceback import traceback_exception_string
from cvp.imgui.begin_child import begin_child_context
from cvp.imgui.button import button
from cvp.imgui.fit_size import FIT_SIZE, FIT_WIDTH
from cvp.imgui.flags.child import BORDERS, RESIZE_X
from cvp.imgui.input_text_multiline import input_text_multiline
from cvp.imgui.input_text_with_hint import input_text_with_hint
from cvp.imgui.text_centered import text_centered
from cvp.imgui.tooltip import hovered_tooltip_text
from cvp.types.override import override


class BinaryMode(BaseMode):
    __cvp_mode_name__ = "Binary-to-Text"
    __cvp_mode_icon__ = HEXADECIMAL

    _MENU_SPLIT_X: Final[int] = 300
    _MENU_CHILD_FLAGS: Final[int] = RESIZE_X | BORDERS

    _SEPARATOR_LABEL: Final[str] = "--"

    _input_error: Optional[BaseException]
    _output_error: Optional[BaseException]

    @unique
    class _TranscodeDirection(Enum):
        encoding = auto()
        decoding = auto()

    def __init__(self, context: Context):
        super().__init__(context)
        self._methods = [str(m) for m in BinaryToText]
        self._encodings = list(ENCODINGS - set(self._methods))
        self._encodings.sort()

        self._filter = str()
        self._input = str()
        self._output = str()
        self._input_error = None
        self._output_error = None
        self._encoding = "utf-8"
        self._errors = "strict"
        self._last_transcoding = self._TranscodeDirection.encoding
        self._default_method = BinaryToText.base64

    def get_selected_method(
        self,
        method_name: Optional[str] = None,
    ) -> Union[BinaryToText, str]:
        if not method_name:
            method_name = self.selected_submenu
        assert isinstance(method_name, str)

        try:
            index = self._methods.index(method_name)
            return BinaryToText(self._methods[index])
        except ValueError:
            pass

        try:
            index = self._encodings.index(method_name)
            return self._encodings[index]
        except ValueError:
            pass

        return self._default_method

    def _encode_with_method(self, method: BinaryToText, value: str) -> str:
        data = value.encode(encoding=self._encoding, errors=self._errors)
        return binary_to_text_encoding(method, data)

    def _encode_with_codec(self, method: str, value: str) -> str:
        data = value.encode(encoding=self._encoding, errors=self._errors)
        try:
            return data.decode(encoding=encodings.normalize_encoding(method))
        except LookupError:
            # noinspection PyTypeChecker
            encoded_data = codecs.encode(data, method)  # type: ignore[call-overload]
            if not isinstance(encoded_data, bytes):
                typename = type(encoded_data).__name__
                raise TypeError(f"Unsupported encoded data type: {typename}")
            return encoded_data.hex()

    def update_encode(self, method: Union[BinaryToText, str], value: str) -> None:
        self._input = value
        self._input_error = None

        try:
            if isinstance(method, BinaryToText):
                self._output = self._encode_with_method(method, value)
            else:
                self._output = self._encode_with_codec(method, value)
            self._output_error = None
        except BaseException as e:
            self._output = str()
            self._output_error = e
        finally:
            self._last_transcoding = self._TranscodeDirection.encoding

    def _decode_with_method(self, method: BinaryToText, value: str) -> str:
        data = binary_to_text_decoding(method, value)
        return data.decode(encoding=self._encoding, errors=self._errors)

    def _decode_with_codec(self, method: str, value: str) -> str:
        method = encodings.normalize_encoding(method)
        try:
            data = value.encode(encoding=method)
        except LookupError:
            decoded_value = codecs.decode(bytes.fromhex(value), method)
            if not isinstance(decoded_value, bytes):
                typename = type(decoded_value).__name__
                raise TypeError(f"Unsupported decoded data type: {typename}")
            data = decoded_value
        return data.decode(encoding=self._encoding, errors=self._errors)

    def update_decode(self, method: Union[BinaryToText, str], value: str) -> None:
        self._output = value
        self._output_error = None

        try:
            if isinstance(method, BinaryToText):
                self._input = self._decode_with_method(method, value)
            else:
                self._input = self._decode_with_codec(method, value)
            self._input_error = None
        except BaseException as e:
            self._input = str()
            self._input_error = e
        finally:
            self._last_transcoding = self._TranscodeDirection.decoding

    def update_with_last_transcoding(self, method: Union[BinaryToText, str]) -> None:
        match self._last_transcoding:
            case self._TranscodeDirection.encoding:
                self.update_encode(method, self._input)
            case self._TranscodeDirection.decoding:
                self.update_decode(method, self._output)

    def clear_fields(self) -> None:
        self._input = str()
        self._output = str()
        self._input_error = None
        self._output_error = None

    @staticmethod
    def convert_displayable_text(method_name: str) -> str:
        return method_name.replace("_", "-").upper()

    @override
    def on_process(self) -> None:
        with self.begin_mode_context():
            if imgui.is_window_appearing():
                self.update_with_last_transcoding(self.get_selected_method())

            self.do_child_process()

    @property
    def method_names(self):
        result = list()
        result.extend(self._methods)

        if not self.context.debug:
            result.remove(str(BinaryToText.mime))
            if sys.version_info < (3, 13):
                result.remove(str(BinaryToText.z85))

        if self.context.debug:
            result.append(self._SEPARATOR_LABEL)
            result.extend(self._encodings)

        return result

    def do_child_process(self) -> None:
        with begin_child_context(
            label="Menu",
            size=(self._MENU_SPLIT_X, 0),
            child_flags=self._MENU_CHILD_FLAGS,
        ):
            imgui.set_next_item_width(FIT_WIDTH)
            self._filter = input_text_with_hint(
                label="##Filter",
                hint="Type to filter the list",
                value=self._filter,
            ).value

            if imgui.begin_list_box("##List", FIT_SIZE):
                try:
                    for method_name in self.method_names:
                        if not self._filter and method_name == self._SEPARATOR_LABEL:
                            imgui.separator()
                            continue

                        display = self.convert_displayable_text(method_name)
                        label = f"{display}##{method_name}"
                        if self._filter:
                            normalized_label = label.lower().strip()
                            normalized_filter = self._filter.lower().strip()
                            if normalized_label.find(normalized_filter) == -1:
                                continue

                        selected = method_name == self.selected_submenu
                        if imgui.selectable(label, selected)[1]:
                            if self.selected_submenu != method_name:
                                selected_method = self.get_selected_method(method_name)
                                self.update_with_last_transcoding(selected_method)
                            self.selected_submenu = method_name
                finally:
                    imgui.end_list_box()

        imgui.same_line()

        with begin_child_context("Main"):
            if method := self.get_selected_method():
                self.do_method_process(method)
            else:
                text_centered("Please select a item")

    def do_method_process(self, method: Union[BinaryToText, str]) -> None:
        display = self.convert_displayable_text(method)
        imgui.text(f"Binary To Text : {display}")
        imgui.separator()

        available_space = imgui.get_content_region_avail()
        item_spacing = imgui.get_style().item_spacing
        total_empty_width = item_spacing.x * 2.0  # center and right padding
        half_width = (available_space.x - total_empty_width) / 2.0

        with begin_child_context("MainLeft", (half_width, 0), RESIZE_X):
            imgui.text("Input")

            if button("Clipboard"):
                self.update_encode(method, imgui.get_clipboard_text())
            imgui.same_line()
            if button("Copy"):
                imgui.set_clipboard_text(self._input)
            imgui.same_line()
            if button("Clear"):
                self.clear_fields()

            if self._input_error is not None:
                self.text_error(str(self._input_error))
                if self.context.debug:
                    hovered_tooltip_text(traceback_exception_string(self._input_error))
            else:
                input_result = input_text_multiline("##Input", self._input, FIT_SIZE)
                if self._input != input_result.value:
                    self.update_encode(method, input_result.value)

        imgui.same_line()

        with begin_child_context("MainBottom"):
            imgui.text("Output")

            disable = self._output_error is not None
            if button("Clipboard", disabled=disable):
                self.update_decode(method, imgui.get_clipboard_text())
            imgui.same_line()
            if button("Copy", disabled=disable):
                imgui.set_clipboard_text(self._output)
            imgui.same_line()
            if button("Clear", disabled=disable):
                self.clear_fields()

            if self._output_error is not None:
                self.text_error(str(self._output_error))
                if self.context.debug:
                    hovered_tooltip_text(traceback_exception_string(self._output_error))
            else:
                output_result = input_text_multiline("##Output", self._output, FIT_SIZE)
                if self._output != output_result.value:
                    self.update_decode(method, output_result.value)
