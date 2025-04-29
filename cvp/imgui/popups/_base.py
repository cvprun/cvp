# -*- coding: utf-8 -*-

from abc import ABC, abstractmethod
from typing import (
    Callable,
    Generic,
    Optional,
    Protocol,
    TypeVar,
    Union,
    runtime_checkable,
)
from uuid import uuid4

from imgui_bundle import imgui

from cvp.imgui.flags.condition import APPEARING
from cvp.imgui.flags.window import WindowFlags
from cvp.imgui.set_window_min_size import set_window_min_size
from cvp.types.override import override

ResultT = TypeVar("ResultT")


class PopupInterface(Generic[ResultT], ABC):
    @abstractmethod
    def get_min_width(self) -> int:
        raise NotImplementedError

    @abstractmethod
    def get_min_height(self) -> int:
        raise NotImplementedError

    @abstractmethod
    def on_process(self) -> Optional[ResultT]:
        raise NotImplementedError


@runtime_checkable
class PopupProtocol(Protocol):
    __cvp_popup_min_width__: int
    __cvp_popup_min_height__: int


class PopupBase(PopupInterface[ResultT], PopupProtocol):
    _target: Optional[Callable[[ResultT], None]]
    _result: Optional[ResultT]

    def __init__(
        self,
        title: Optional[str] = None,
        flags: Union[WindowFlags, int] = 0,
        *,
        target: Optional[Callable[[ResultT], None]] = None,
        oneshot: Optional[bool] = None,
        identifier: Optional[str] = None,
        min_width: Optional[int] = None,
        min_height: Optional[int] = None,
        centered=True,
    ):
        if isinstance(flags, WindowFlags):
            flags = int(flags)
        assert isinstance(flags, int)

        self._title = title if title else type(self).__name__
        self._visible = False
        self._centered = centered
        self._flags = flags
        self._identifier = identifier if identifier else str(uuid4())

        self._min_width = min_width
        self._min_height = min_height

        self._result = None
        self._target = target
        self._oneshot = bool(oneshot)

    @override
    def get_min_width(self) -> int:
        if self._min_width is not None:
            return self._min_width
        else:
            return self.__cvp_popup_min_width__

    @override
    def get_min_height(self) -> int:
        if self._min_height is not None:
            return self._min_height
        else:
            return self.__cvp_popup_min_height__

    @override
    def on_process(self) -> Optional[ResultT]:
        raise NotImplementedError

    @property
    def title(self):
        return self._title

    @property
    def target(self):
        return self._target

    @target.setter
    def target(self, value: Callable[[ResultT], None]) -> None:
        self._target = value

    @property
    def result(self):
        return self._result

    @result.setter
    def result(self, value: Optional[ResultT]) -> None:
        self._result = value

    @property
    def identifier(self):
        return self._identifier

    @property
    def popup_label(self):
        return f"{self._title}###{self._identifier}"

    def show(
        self,
        title: Optional[str] = None,
        target: Optional[Callable[[ResultT], None]] = None,
        oneshot: Optional[bool] = None,
    ) -> None:
        self._visible = True
        if title is not None:
            self._title = title
        if target is not None:
            self._target = target
        if oneshot is not None:
            self._oneshot = oneshot

    def show_oneshot(
        self,
        title: Optional[str] = None,
        target: Optional[Callable[[ResultT], None]] = None,
    ) -> None:
        self.show(title, target, oneshot=True)

    def do_process(self) -> Optional[ResultT]:
        if self._visible:
            imgui.open_popup(self.popup_label)
            self._visible = False

        if self._centered:
            center = imgui.get_main_viewport().get_center()
            x, y = center.x, center.y
            px, py = 0.5, 0.5
            imgui.set_next_window_pos((x, y), APPEARING, (px, py))

        modal = imgui.begin_popup_modal(self.popup_label, None, self._flags)
        if not modal[0]:
            self._result = None
            return None

        if imgui.is_window_appearing():
            set_window_min_size(self.get_min_width(), self.get_min_height())

        try:
            self._result = self.on_process()
            if self._target is not None and self._result is not None:
                self._target(self._result)
                if self._oneshot:
                    self._target = None
            return self._result
        finally:
            imgui.end_popup()
