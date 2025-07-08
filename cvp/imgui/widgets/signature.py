# -*- coding: utf-8 -*-

from dataclasses import dataclass
from inspect import Parameter, signature
from typing import Callable, Dict, NamedTuple, Optional

from imgui_bundle import imgui

from cvp.patterns.singleton import singleton


class InputSignatureResult(NamedTuple):
    pass


@dataclass
class InputSignatureOptions:
    pass


class InputSignature:
    def __init__(
        self,
        label: str,
        function: Callable,
        options: Optional[InputSignatureOptions] = None,
    ):
        self._label = label
        self._function = function
        self._signature = signature(function)
        self._options = options

    @property
    def options(self):
        return self._options

    def input_parameter(self, key: str, parameter: Parameter) -> None:
        annotation = parameter.annotation
        default = parameter.default
        name = parameter.name

        # if isinstance(annotation, str):
        #     if item_result := input_text(f"##Item.{index}", item):
        #         container[index] = item_result.value
        # elif isinstance(item, int):
        #     if item_result := input_int(f"##Item.{index}", item):
        #         container[index] = item_result.value
        # elif isinstance(item, float):
        #     if item_result := input_float(f"##Item.{index}", item):
        #         container[index] = item_result.value
        # else:
        #     imgui.text(str(item))
        #     item_typename = type(item).__name__

    def do_process(self) -> InputSignatureResult:
        result = InputSignatureResult()

        for key, param in self._signature.parameters.items():
            self.input_parameter(key, param)

        return result


@singleton
class GlobalInputSignatureOptions(Dict[int, InputSignatureOptions]):
    pass


def input_signature(
    label: str,
    function: Callable,
    options: Optional[InputSignatureOptions] = None,
):
    if options is None:
        global_options = GlobalInputSignatureOptions()
        next_id = imgui.get_id(label)
        options = global_options.get(next_id)
        if options is None:
            options = InputSignatureOptions()
            global_options.__setitem__(next_id, options)

    return InputSignature(label, function, options).do_process()
