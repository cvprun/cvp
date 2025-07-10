# -*- coding: utf-8 -*-

from inspect import Parameter, signature
from typing import Any, Callable, List, Optional, Tuple

from imgui_bundle import imgui

from cvp.imgui.text_colored import text_colored
from cvp.inspect.argument import Argument, ArgumentMapper
from cvp.memory.copy import copy_method, copy_with_method
from cvp.types.colors import RED_RGBA, RGBA
from cvp.variables import MODULE_PATH_SEPARATOR, NOT_FOUND_INDEX


class InputSignature:
    def __init__(
        self,
        label: str,
        function: Callable[..., Any],
        arguments: Optional[ArgumentMapper] = None,
        error_color: Optional[RGBA] = None,
        *,
        use_copy=False,
        use_deepcopy=False,
    ):
        self._label = label
        self._error_color = error_color if error_color else RED_RGBA
        self._separator = MODULE_PATH_SEPARATOR
        self._copy_method = copy_method(use_copy=use_copy, use_deepcopy=use_deepcopy)

        if arguments is None:
            parameters = signature(function).parameters
            arguments = ArgumentMapper.from_parameters(parameters)
            for key, param in parameters.items():
                if key not in arguments:
                    arguments[key] = Argument(param)

        self._arguments = arguments

    @property
    def arguments(self):
        return self._arguments

    def value_key(self, name: str, parent: str) -> str:
        return f"{parent}{self._separator}{name}" if parent else name

    def label_key(self, name: str, parent: str) -> Tuple[str, str]:
        key = self.value_key(name, parent)
        label = f"{name}###{key}"
        return label, key

    def text_error(self, text: str) -> None:
        text_colored(text, self._error_color)

    def do_root_argument(self, argument: Argument) -> bool:
        cls = argument.type_deduction()
        try:
            argument.value = self.do_argument(cls, argument)
            return True
        except BaseException as e:
            typename = cls.__name__ if isinstance(cls, type) else str(cls)
            self.text_error(f"{argument.name} <{typename}> {e}")
            return False

    def do_argument(self, cls: Any, argument: Argument) -> Any:
        name = argument.name
        parent = str()

        if cls is None:
            return self.do_none(name, None, parent)

        if isinstance(cls, type):
            if issubclass(cls, bool):
                return self.do_boolean(name, argument.get_value(False), parent)
            elif issubclass(cls, int):
                return self.do_integer(name, argument.get_value(0), parent)
            elif issubclass(cls, float):
                return self.do_floating(name, argument.get_value(0.0), parent)
            elif issubclass(cls, str):
                return self.do_string(name, argument.get_value(str()), parent)

        raise TypeError(f"Cannot find handler for {cls}")

    def do_none(self, name: str, value: Any, parent: str) -> None:
        if value == Parameter.empty:
            value = None
        assert value is None
        label, key = self.label_key(name, parent)
        imgui.text(label)
        return None

    def do_boolean(self, name: str, value: Any, parent: str) -> bool:
        if value in (None, Parameter.empty):
            value = False
        assert isinstance(value, bool)
        label, key = self.label_key(name, parent)
        changed, value = imgui.checkbox(label, value)
        assert isinstance(changed, bool)
        assert isinstance(value, bool)
        return value

    def do_integer(self, name: str, value: Any, parent: str) -> int:
        if value in (None, Parameter.empty):
            value = 0
        assert isinstance(value, int)
        label, key = self.label_key(name, parent)
        changed, value = imgui.input_int(label, value)
        assert isinstance(changed, bool)
        assert isinstance(value, int)
        return value

    def do_floating(self, name: str, value: Any, parent: str) -> float:
        if value in (None, Parameter.empty):
            value = 0.0
        assert isinstance(value, float)
        label, key = self.label_key(name, parent)
        changed, value = imgui.input_float(label, value)
        assert isinstance(changed, bool)
        assert isinstance(value, float)
        return value

    def do_string(self, name: str, value: Any, parent: str) -> str:
        if value in (None, Parameter.empty):
            value = str()
        assert isinstance(value, str)
        label, key = self.label_key(name, parent)
        changed, value = imgui.input_text(label, value)
        assert isinstance(changed, bool)
        assert isinstance(value, str)
        return value

    def do_combo(
        self,
        name: str,
        value: Any,
        parent: str,
        choices: List[str],
    ) -> str:
        assert choices
        if value in (None, Parameter.empty):
            value = choices[0]
        assert isinstance(value, str)
        label, key = self.label_key(name, parent)
        try:
            choice_index = choices.index(value)
        except ValueError:
            choice_index = NOT_FOUND_INDEX
        changed, current = imgui.combo(label, choice_index, choices)
        assert isinstance(changed, bool)
        assert isinstance(current, int)
        return choices[current] if changed else value

    def do_process(self) -> ArgumentMapper:
        for key, argument in self._arguments.items():
            self.do_root_argument(argument)
        return copy_with_method(self._arguments, self._copy_method)


def input_signature(
    label: str,
    function: Callable[..., Any],
    arguments: ArgumentMapper,
    error_color: Optional[RGBA] = None,
    *,
    use_copy=False,
    use_deepcopy=False,
):
    widget = InputSignature(
        label=label,
        function=function,
        arguments=arguments,
        error_color=error_color,
        use_copy=use_copy,
        use_deepcopy=use_deepcopy,
    )
    return widget.do_process()
