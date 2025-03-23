# -*- coding: utf-8 -*-

from typing import Any, Callable, Dict, Generic, Optional, Tuple, TypeVar

from imgui_bundle import imgui
from pygame.event import Event

from cvp.config.sections.bases.window import WindowConfig
from cvp.imgui.able.pressable import Pressable
from cvp.imgui.flags import button, window
from cvp.imgui.set_window_min_size import set_window_min_size
from cvp.logging.logging import logger
from cvp.msgs.callbacks import MsgCallbacks
from cvp.msgs.msg import Msg
from cvp.msgs.msg_map import MsgWrapper, create_msg_map
from cvp.msgs.msg_type import MsgTypeLike, get_msg_type_number
from cvp.pygame.able.eventable import Eventable
from cvp.pygame.able.keyboardable import Keyboardable
from cvp.pygame.able.mouseable import Mouseable
from cvp.pygame.constants import Constants
from cvp.pygame.constants.event_type import EventType
from cvp.pygame.events.callbacks import EventCallbacks
from cvp.pygame.events.event_map import EventWrapper, create_event_map
from cvp.renderer.context import RendererContext
from cvp.renderer.popup.base import PopupBase
from cvp.renderer.window.interface import WindowInterface
from cvp.renderer.window.query import WindowQuery
from cvp.types.override import override
from cvp.variables import MIN_WINDOW_HEIGHT, MIN_WINDOW_WIDTH

WindowConfigT = TypeVar("WindowConfigT", bound=WindowConfig)


class WindowBase(
    Generic[WindowConfigT],
    Pressable,
    WindowInterface,
    EventCallbacks,
    MsgCallbacks,
    Eventable,
    Keyboardable,
    Mouseable,
    Constants,
):
    _popups: Dict[str, PopupBase]
    _events: Dict[int, EventWrapper]
    _msgs: Dict[int, MsgWrapper]

    def __init__(
        self,
        context: RendererContext,
        window_config: WindowConfigT,
        title: Optional[str] = None,
        closable: Optional[bool] = None,
        flags: Optional[int] = None,
        min_width=MIN_WINDOW_WIDTH,
        min_height=MIN_WINDOW_HEIGHT,
        modifiable_title=False,
    ) -> None:
        self._context = context
        self._window_config = window_config
        self._title = title if title else type(self).__name__

        if not self._window_config.title:
            self._window_config.title = self._title

        self.closable = closable if closable else False
        self.flags = flags if flags else 0

        self._min_width = min_width
        self._min_height = min_height
        self._modifiable_title = modifiable_title

        self._initialized = False
        self._removable = False
        self._popups = dict()
        self._events = dict()
        self._msgs = dict()
        self._query = WindowQuery()

        self._appeared = False
        self._focused = False
        self._hovered = False
        self._shown = False
        self._expanded = False

    def _has_flag(self, flag: int) -> bool:
        return bool(self.flags & flag)

    def _set_flag(self, flag: int, enable: bool) -> None:
        if enable:
            self.flags |= flag
        else:
            self.flags &= ~flag

    @property
    def no_titlebar(self) -> bool:
        return self._has_flag(window.NO_TITLE_BAR)

    @no_titlebar.setter
    def no_titlebar(self, value: bool) -> None:
        self._set_flag(window.NO_TITLE_BAR, value)

    @property
    def no_scrollbar(self) -> bool:
        return self._has_flag(window.NO_SCROLLBAR)

    @no_scrollbar.setter
    def no_scrollbar(self, value: bool) -> None:
        self._set_flag(window.NO_SCROLLBAR, value)

    @property
    def no_menu(self) -> bool:
        return not self._has_flag(window.MENU_BAR)

    @no_menu.setter
    def no_menu(self, value: bool) -> None:
        self._set_flag(window.MENU_BAR, not value)

    @property
    def no_move(self) -> bool:
        return self._has_flag(window.NO_MOVE)

    @no_move.setter
    def no_move(self, value: bool) -> None:
        self._set_flag(window.NO_MOVE, value)

    @property
    def no_resize(self) -> bool:
        return self._has_flag(window.NO_RESIZE)

    @no_resize.setter
    def no_resize(self, value: bool) -> None:
        self._set_flag(window.NO_RESIZE, value)

    @property
    def no_collapse(self) -> bool:
        return self._has_flag(window.NO_COLLAPSE)

    @no_collapse.setter
    def no_collapse(self, value: bool) -> None:
        self._set_flag(window.NO_COLLAPSE, value)

    @property
    def no_nav(self) -> bool:
        return self._has_flag(window.NO_NAV)

    @no_nav.setter
    def no_nav(self, value: bool) -> None:
        self._set_flag(window.NO_NAV, value)

    @property
    def no_background(self) -> bool:
        return self._has_flag(window.NO_BACKGROUND)

    @no_background.setter
    def no_background(self, value: bool) -> None:
        self._set_flag(window.NO_BACKGROUND, value)

    @property
    def no_bring_to_front(self) -> bool:
        return self._has_flag(window.NO_BRING_TO_FRONT_ON_FOCUS)

    @no_bring_to_front.setter
    def no_bring_to_front(self, value: bool) -> None:
        self._set_flag(window.NO_BRING_TO_FRONT_ON_FOCUS, value)

    @property
    def unsaved_document(self) -> bool:
        return self._has_flag(window.UNSAVED_DOCUMENT)

    @unsaved_document.setter
    def unsaved_document(self, value: bool) -> None:
        self._set_flag(window.UNSAVED_DOCUMENT, value)

    @property
    def window_config(self):
        return self._window_config

    @property
    def initialized(self) -> bool:
        return self._initialized

    @property
    def removable(self) -> bool:
        return self._removable

    def set_removable(self) -> None:
        self._removable = True
        logger.debug(
            f"{repr(self)} "
            "The 'removable' flag is enabled. "
            "The destroy event is called just before the next loop execution."
        )

    @property
    def opened(self) -> bool:
        return self._window_config.opened

    @opened.setter
    def opened(self, value: bool) -> None:
        self._window_config.opened = value

    def open(self) -> None:
        self._window_config.opened = True

    def close(self) -> None:
        self._window_config.opened = False

    def flip_opened(self) -> None:
        self._window_config.opened = not self._window_config.opened

    @property
    def title(self) -> str:
        if self._modifiable_title:
            return self._window_config.title
        else:
            return self._title

    @title.setter
    def title(self, value: str) -> None:
        if not self._modifiable_title:
            logger.warning(
                f"{repr(self)} "
                "The title of a window that cannot be renamed should not be changed"
            )
        self._window_config.title = value

    @property
    def query(self):
        return self._query

    @property
    def focused(self):
        return self._focused

    @property
    def hovered(self):
        return self._hovered

    def is_mouse_button_clicked(self, button_index: int) -> bool:
        if not self.hovered:
            return False
        return imgui.is_mouse_clicked(button_index)

    def is_mouse_left_button_clicked(self) -> bool:
        return self.is_mouse_button_clicked(button.MOUSE_BUTTON_LEFT)

    def is_mouse_middle_button_clicked(self) -> bool:
        return self.is_mouse_button_clicked(button.MOUSE_BUTTON_MIDDLE)

    def is_mouse_right_button_clicked(self) -> bool:
        return self.is_mouse_button_clicked(button.MOUSE_BUTTON_RIGHT)

    @property
    @override
    def context(self):
        return self._context

    @property
    @override
    def key(self):
        return self.window_config.uuid

    @property
    @override
    def label(self) -> str:
        return f"{self.title}###{self.key}"

    def __repr__(self) -> str:
        return f"<{type(self).__name__} key={self.key}>"

    def __str__(self) -> str:
        return self.label

    @override
    def begin(self) -> Tuple[bool, bool]:
        expanded, opened = imgui.begin(self.label, self.closable, self.flags)
        assert isinstance(expanded, bool)
        assert isinstance(opened, bool)
        return expanded, opened

    @override
    def end(self) -> None:
        imgui.end()

    @override
    def on_create(self) -> None:
        logger.debug(f"{repr(self)} Empty create event")

    @override
    def on_destroy(self) -> None:
        logger.debug(f"{repr(self)} Empty destroy event")

    @override
    def on_appearing(self) -> None:
        logger.debug(f"{repr(self)} Empty appearing event")

    @override
    def on_disappeared(self) -> None:
        logger.debug(f"{repr(self)} Empty disappeared event")

    @override
    def on_focused(self) -> None:
        logger.debug(f"{repr(self)} Empty focused event")

    @override
    def on_unfocused(self) -> None:
        logger.debug(f"{repr(self)} Empty unfocused event")

    @override
    def on_hovered(self) -> None:
        logger.debug(f"{repr(self)} Empty hovered event")

    @override
    def on_unhovered(self) -> None:
        logger.debug(f"{repr(self)} Empty unhovered event")

    @override
    def on_shown(self):
        logger.debug(f"{repr(self)} Empty shown event")

    @override
    def on_hidden(self):
        logger.debug(f"{repr(self)} Empty hidden event")

    @override
    def on_expanded(self):
        logger.debug(f"{repr(self)} Empty expanded event")

    @override
    def on_unexpanded(self):
        logger.debug(f"{repr(self)} Empty unexpanded event")

    @override
    def on_event(self, event: Event) -> Optional[bool]:
        pass

    @override
    def on_msg(self, msg: Msg) -> Optional[bool]:
        pass

    @override
    def on_before(self) -> None:
        pass

    @override
    def on_process(self) -> None:
        pass

    @override
    def on_after(self) -> None:
        pass

    @override
    def on_popup(self, popup: PopupBase, result: Any) -> None:
        pass

    def register_popup(self, popup: PopupBase) -> None:
        self._popups[popup.title] = popup

    def unregister_popup(self, popup: PopupBase) -> None:
        self._popups.pop(popup.title)

    def register_event_callback(
        self,
        event_type: EventType,
        callback: Callable,
    ) -> None:
        self._events[event_type].append_callback(callback)

    def register_msg_callback(self, msg_type: MsgTypeLike, callback: Callable) -> None:
        self._msgs[get_msg_type_number(msg_type)].append_callback(callback)

    def update_event_map(self, obj: Any, cls: type) -> None:
        self._events.update(create_event_map(obj, cls))

    def update_msg_map(self, obj: Any, cls: type) -> None:
        self._msgs.update(create_msg_map(obj, cls))

    def toast(self, message: str) -> None:
        self._context.mq.append_toast(message)

    def do_create(self) -> None:
        if self._initialized:
            raise ValueError("Already initialized window instance")

        self._events.update(create_event_map(self))
        self._msgs.update(create_msg_map(self))

        try:
            self.on_create()
        except BaseException as e:
            logger.error(f"{repr(self)} {e}")
            raise e

        self._initialized = True
        logger.info(f"{repr(self)} The constructor has been called")

    def do_destroy(self) -> None:
        if not self._initialized:
            raise ValueError("The window instance is not initialized")

        try:
            self.on_destroy()
        except BaseException as e:
            logger.error(f"{repr(self)} {e}")
            raise e

        self._events.clear()
        self._initialized = False
        logger.info(f"{repr(self)} The destructor has been called")

    def do_event(self, event: Event) -> Optional[bool]:
        if not self._initialized:
            raise ValueError("The window instance is not initialized")

        if bool(self.on_event(event)):
            return True

        return self._events[event.type](event)

    def do_msg(self, msg: Msg) -> Optional[bool]:
        if not self._initialized:
            raise ValueError("The window instance is not initialized")

        if bool(self.on_msg(msg)):
            return True

        return self._msgs[get_msg_type_number(msg.mtype)](msg)

    def do_appeared(self) -> None:
        if self._appeared:
            return
        self._appeared = True
        self.on_appearing()

    def do_disappeared(self) -> None:
        if not self._appeared:
            return
        self._appeared = False
        self.on_disappeared()

    def do_focused(self) -> None:
        if self._focused:
            return
        self._focused = True
        self._context.config.window_manager.appendleft_begin_order(self.key)
        self.on_focused()

    def do_unfocused(self) -> None:
        if not self._focused:
            return
        self._focused = False
        self.on_unfocused()

    def do_hovered(self) -> None:
        if self._hovered:
            return
        self._hovered = True
        self.on_hovered()

    def do_unhovered(self) -> None:
        if not self._hovered:
            return
        self._hovered = False
        self.on_unhovered()

    def do_shown(self) -> None:
        if self._shown:
            return
        self._shown = True
        self.on_shown()

    def do_hidden(self) -> None:
        if not self._shown:
            return
        self._shown = False
        self.on_hidden()

    def do_expanded(self) -> None:
        if self._expanded:
            return
        self._expanded = True
        self.on_expanded()

    def do_unexpanded(self) -> None:
        if not self._expanded:
            return
        self._expanded = False
        self.on_unexpanded()

    def do_popup_process(self):
        for popup in self._popups.values():
            result = popup.do_process()
            if result is not None:
                self.on_popup(popup, result)

    def do_process(self) -> None:
        if not self._initialized:
            raise ValueError("The window instance is not initialized")

        if not self.opened:
            self.do_disappeared()
            self.do_unfocused()
            self.do_unhovered()
            self.do_hidden()
            return

        self.on_before()
        try:
            expanded, opened = self.begin()
            self._query.update(expanded, opened)

            try:
                if self._query.appearing:
                    set_window_min_size(self._min_width, self._min_height)
                    self.do_appeared()

                if self._query.focused:
                    self.do_focused()
                else:
                    self.do_unfocused()

                if self._query.hovered:
                    self.do_hovered()
                else:
                    self.do_unhovered()

                if self._query.opened:
                    self.do_shown()
                else:
                    self.do_hidden()
                    self.opened = False
                    return

                if self._query.expanded:
                    self.do_expanded()
                else:
                    self.do_unexpanded()
                    return

                self.on_process()
            finally:
                self.end()

            self.do_popup_process()
        finally:
            self.on_after()
