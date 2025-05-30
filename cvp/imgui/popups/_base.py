# -*- coding: utf-8 -*-

from abc import ABC, abstractmethod
from typing import (
    Callable,
    Optional,
    Protocol,
    Union,
    runtime_checkable,
)
from uuid import uuid4

from imgui_bundle import imgui

from cvp.imgui.flags.condition import APPEARING
from cvp.imgui.flags.window import WindowFlags
from cvp.imgui.popups.interface import PopupInterface, PopupResultT
from cvp.imgui.set_window_min_size import set_window_min_size
from cvp.types.override import override


class PopupBaseInterface(PopupInterface[PopupResultT], ABC):
    @abstractmethod
    def on_main_process(self) -> Optional[PopupResultT]:
        raise NotImplementedError


@runtime_checkable
class PopupProtocol(Protocol):
    __cvp_popup_min_width__: int
    __cvp_popup_min_height__: int


class PopupBase(PopupBaseInterface[PopupResultT], PopupProtocol, ABC):
    _target: Optional[Callable[[PopupResultT], None]]
    _result: Optional[PopupResultT]

    def __init__(
        self,
        title: Optional[str] = None,
        flags: Union[WindowFlags, int] = 0,
        *,
        target: Optional[Callable[[PopupResultT], None]] = None,
        oneshot: Optional[bool] = None,
        identifier: Optional[str] = None,
        min_width: Optional[int] = None,
        min_height: Optional[int] = None,
        centered=True,
    ):
        if isinstance(flags, WindowFlags):
            flags = int(flags)
        assert isinstance(flags, int)
        assert isinstance(self, PopupProtocol)

        self._title = title if title else type(self).__name__
        self._centered = centered
        self._flags = flags
        self._identifier = identifier if identifier else str(uuid4())

        self._min_width = min_width
        self._min_height = min_height

        self._result = None
        self._target = target
        self._oneshot = bool(oneshot)

        self._visible = False
        self._opened = False
        self._closeable = False

    @override
    def is_opened(self) -> bool:
        return self._opened

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

    @property
    def opened(self) -> bool:
        return self.is_opened()

    @property
    def title(self):
        return self._title

    @property
    def target(self):
        return self._target

    @target.setter
    def target(self, value: Callable[[PopupResultT], None]) -> None:
        self._target = value

    @property
    def result(self):
        return self._result

    @result.setter
    def result(self, value: Optional[PopupResultT]) -> None:
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
        target: Optional[Callable[[PopupResultT], None]] = None,
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
        target: Optional[Callable[[PopupResultT], None]] = None,
    ) -> None:
        self.show(title, target, oneshot=True)

    def close(self) -> None:
        if not self._closeable:
            raise ValueError(
                f"Calling '{self.close.__name__}' is only allowed in the"
                f" '{self.on_main_process.__name__}' callback"
            )

        imgui.close_current_popup()

    @override
    def on_process(self) -> Optional[PopupResultT]:
        self._opened = imgui.is_popup_open(self.popup_label)

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
            self._closeable = True
            try:
                self._result = self.on_main_process()
            finally:
                self._closeable = False

            if self._target is not None and self._result is not None:
                self._target(self._result)
                if self._oneshot:
                    self._target = None

            return self._result
        finally:
            imgui.end_popup()
