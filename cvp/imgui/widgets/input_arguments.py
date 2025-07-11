# -*- coding: utf-8 -*-

from datetime import date, datetime, time
from inspect import Parameter, signature
from typing import (
    Any,
    Callable,
    List,
    Optional,
    Tuple,
    TypeVar,
    Union,
    get_args,
    get_origin,
)

from imgui_bundle import imgui

from cvp.imgui.drag_date import drag_date
from cvp.imgui.input_time import input_time
from cvp.imgui.text_colored import text_colored
from cvp.inspect.argument import Argument, ArgumentMapper
from cvp.memory.copy import copy_flexible, copy_method, copy_with_method
from cvp.types.colors import RED_RGBA, RGBA
from cvp.variables import MODULE_PATH_SEPARATOR, NOT_FOUND_INDEX

_T = TypeVar("_T")


class BaseInputArguments:
    def __init__(
        self,
        separator=MODULE_PATH_SEPARATOR,
        error_color: Optional[RGBA] = None,
    ):
        self._separator = separator
        self._error_color = error_color if error_color else RED_RGBA

    def value_key(self, name: str, parent: str, *, suffix: Optional[str] = None) -> str:
        prefix = f"{parent}{self._separator}{name}" if parent else name
        return f"{prefix}{self._separator}{suffix}" if suffix else prefix

    def label_key(self, name: str, parent: str) -> Tuple[str, str]:
        key = self.value_key(name, parent)
        label = f"{name}###{key}"
        return label, key

    def text_error(self, text: str) -> None:
        text_colored(text, self._error_color)

    def do_root_arguments(
        self,
        arguments: ArgumentMapper,
        *,
        use_copy=False,
        use_deepcopy=False,
    ) -> ArgumentMapper:
        for key, argument in arguments.items():
            self.do_root_argument(argument)
        return copy_flexible(arguments, use_copy=use_copy, use_deepcopy=use_deepcopy)

    def do_root_argument(self, argument: Argument, *, raise_errors=False) -> bool:
        cls = argument.type_deduction()
        try:
            argument.value = self.do_argument(cls, argument)
            return True
        except BaseException as e:
            if raise_errors:
                raise

            typename = cls.__name__ if isinstance(cls, type) else str(cls)
            self.text_error(f"{argument.name} <{typename}> {e}")
            return False

    def do_argument(self, cls: Any, argument: Argument) -> Any:
        name = argument.name
        parent = str()
        use_none = False

        if cls is None:
            return self.do_none(name, None, parent)

        if cls == Union:
            type_annotation = argument.annotation
            assert get_origin(type_annotation) == Union
            type_args = get_args(type_annotation)

            union_types = list(type_args)
            assert 2 <= len(union_types)

            if 2 == len(union_types) and type(None) in union_types:
                union_types.remove(type(None))
                assert 1 == len(union_types)
                cls = union_types[0]
                _, use_none = self.do_optional(cls, argument.get_value(None), parent)
                imgui.same_line()
            else:
                assert 2 <= len(union_types)
                # _, use_none = self.do_union_types(cls, union_types, parent)
                # imgui.same_line()
                # for union_type in union_types:
                #     pass
                raise TypeError(f"Cannot deduce type from UNION: {union_types}")

        if not isinstance(cls, type):
            raise TypeError(f"Cannot find handler for {cls}")

        result: Any
        name = argument.name
        imgui.begin_disabled(disabled=use_none)
        try:
            if issubclass(cls, bool):
                result = self.do_boolean(name, argument.get_value(False), parent)
            elif issubclass(cls, int):
                result = self.do_integer(name, argument.get_value(0), parent)
            elif issubclass(cls, float):
                result = self.do_floating(name, argument.get_value(0.0), parent)
            elif issubclass(cls, str):
                result = self.do_string(name, argument.get_value(str()), parent)
            elif issubclass(cls, date):
                result = self.do_date(name, argument.get_value(date.today()), parent)
            else:
                raise TypeError(f"Cannot find handler for {cls}")
        finally:
            imgui.end_disabled()

        return None if use_none else result

    def do_none(self, name: str, value: Any, parent: str) -> None:
        if value == Parameter.empty:
            value = None
        assert value is None
        label, key = self.label_key(name, parent)
        imgui.text(label)
        return None

    def do_optional(self, name: str, value: Any, parent: str):
        key = self.value_key(name, parent, suffix="Optional")
        none_changed, none_enabled = imgui.checkbox(f"Optional##{key}", value is None)
        assert isinstance(none_changed, bool)
        assert isinstance(none_enabled, bool)
        return none_changed, none_enabled

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

    def do_date(self, name: str, value: Any, parent: str) -> date:
        if value in (None, Parameter.empty):
            value = date.today()
        assert isinstance(value, date)
        label, key = self.label_key(name, parent)
        changed, value = drag_date(label, value)
        assert isinstance(changed, bool)
        assert isinstance(value, date)
        return value

    def do_time(self, name: str, value: Any, parent: str) -> time:
        if value in (None, Parameter.empty):
            value = datetime.now().time()
        assert isinstance(value, time)
        label, key = self.label_key(name, parent)
        changed, value = input_time(label, value)
        assert isinstance(changed, bool)
        assert isinstance(value, time)
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


class InputArguments(BaseInputArguments):
    def __init__(
        self,
        function: Callable[..., Any],
        arguments: Optional[ArgumentMapper] = None,
        *,
        separator=MODULE_PATH_SEPARATOR,
        error_color: Optional[RGBA] = None,
        use_copy=False,
        use_deepcopy=False,
    ):
        super().__init__(separator=separator, error_color=error_color)

        if arguments is None:
            parameters = signature(function).parameters
            arguments = ArgumentMapper.from_parameters(parameters)

        self._arguments = arguments
        self._copy_method = copy_method(use_copy=use_copy, use_deepcopy=use_deepcopy)

    @property
    def arguments(self):
        return self._arguments

    def do_process(self) -> ArgumentMapper:
        result = self.do_root_arguments(
            arguments=self._arguments,
            use_copy=False,
            use_deepcopy=False,
        )
        return copy_with_method(result, self._copy_method)


def input_arguments(
    function: Callable[..., Any],
    arguments: ArgumentMapper,
    error_color: Optional[RGBA] = None,
    *,
    use_copy=False,
    use_deepcopy=False,
):
    widget = InputArguments(
        function=function,
        arguments=arguments,
        error_color=error_color,
        use_copy=use_copy,
        use_deepcopy=use_deepcopy,
    )
    return widget.do_process()
