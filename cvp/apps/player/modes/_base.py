# -*- coding: utf-8 -*-

from datetime import datetime
from typing import Dict, Optional, Protocol, Union, runtime_checkable

from imgui_bundle import imgui
from pygame.event import Event
from pygame.key import ScancodeWrapper

from cvp.apps.player.modes.interface import ModeInterface
from cvp.context.context import Context
from cvp.imgui.begin_mode import begin_mode_context
from cvp.imgui.menu_recent_items import menu_recent_items
from cvp.imgui.tooltip import hovered_tooltip_text_wrapped
from cvp.msgs.callbacks import MsgCallbacks
from cvp.msgs.msg import Msg
from cvp.msgs.msg_map import MsgWrapper, create_msg_map
from cvp.types.override import override


@runtime_checkable
class BaseModeProtocol(Protocol):
    __cvp_mode_name__: str
    __cvp_mode_icon__: str
    __cvp_mode_show__: bool


class BaseMode(ModeInterface, MsgCallbacks, BaseModeProtocol):
    __cvp_mode_show__ = True

    _msg_mapping: Optional[Dict[int, MsgWrapper]]

    def __init__(self, context: Context):
        assert isinstance(self, BaseModeProtocol)
        self._context = context
        self._msg_mapping = None

    @property
    def context(self) -> Context:
        return self._context

    @classmethod
    @override
    def get_mode_name(cls) -> str:
        return cls.__cvp_mode_name__

    @classmethod
    @override
    def get_mode_icon(cls) -> str:
        return cls.__cvp_mode_icon__

    @classmethod
    @override
    def get_mode_show(cls) -> bool:
        return cls.__cvp_mode_show__

    @override
    def on_main_menu(self) -> None:
        pass

    @override
    def on_status_menu(self) -> None:
        pass

    @override
    def on_event(self, event: Event) -> bool:
        return False

    @override
    def on_msg(self, msg: Msg) -> bool:
        if self._msg_mapping is None:
            self._msg_mapping = create_msg_map(self)
        assert self._msg_mapping is not None

        if wrapper := self._msg_mapping.get(msg.mtype):
            assert isinstance(wrapper, MsgWrapper)
            return wrapper(msg)
        else:
            return False

    @override
    def on_keyboard(self, keys: ScancodeWrapper) -> None:
        pass

    @override
    def on_process(self) -> None:
        pass

    @property
    def success_color(self):
        return self.context.config.appearance.success_color

    @property
    def normal_color(self):
        return self.context.config.appearance.normal_color

    @property
    def warning_color(self):
        return self.context.config.appearance.warning_color

    @property
    def error_color(self):
        return self.context.config.appearance.error_color

    def text_success(self, text: str) -> None:
        imgui.text_colored(self.success_color, text)

    def text_normal(self, text: str) -> None:
        imgui.text_colored(self.normal_color, text)

    def text_warning(self, text: str) -> None:
        imgui.text_colored(self.warning_color, text)

    def text_error(self, text: str) -> None:
        imgui.text_colored(self.error_color, text)

    def hovered_tooltip(self, message: Union[str, BaseException]) -> bool:
        if isinstance(message, BaseException):
            return hovered_tooltip_text_wrapped(str(message), self.error_color)
        else:
            assert isinstance(message, str)
            return hovered_tooltip_text_wrapped(message)

    def get_selected_submenu(self, *, suffix=None) -> str:
        return self._context.get_selected_submenu(type(self), suffix=suffix)

    def set_selected_submenu(self, value: str, *, suffix=None) -> None:
        self._context.set_selected_submenu(type(self), value, suffix=suffix)

    @property
    def selected_submenu(self) -> str:
        return self.get_selected_submenu()

    @selected_submenu.setter
    def selected_submenu(self, value: str) -> None:
        self.set_selected_submenu(value)

    def get_recent_items(self, *, suffix=None):
        return self._context.get_recent_items(type(self), suffix=suffix)

    def add_recent_item(
        self,
        value: str,
        accessed_at: Optional[datetime] = None,
        *,
        suffix=None,
    ) -> None:
        self._context.add_recent_item(
            type(self),
            value,
            accessed_at,
            suffix=suffix,
        )

    def menu_recent_items(
        self,
        label="Recent items",
        clear_menu_label="Clear recent items",
    ):
        return menu_recent_items(
            label=label,
            config=self.context.config.navigation,
            cls=type(self),
            append_clear_menu=True,
            clear_menu_label=clear_menu_label,
        )

    def clear_recent_items(self, *, suffix=None) -> None:
        self._context.clear_recent_items(type(self), suffix=suffix)

    def begin_mode_context(self):
        return begin_mode_context(type(self).__name__)

    def run_with_single_mode(self):
        imgui.begin_main_menu_bar()
        try:
            self.on_main_menu()
        finally:
            imgui.end_main_menu_bar()
        self.on_process()
