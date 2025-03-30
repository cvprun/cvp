# -*- coding: utf-8 -*-

from collections import OrderedDict
from typing import Callable

from imgui_bundle import imgui
from pygame.event import Event
from pygame.key import ScancodeWrapper

from cvp.apps.player.modes._base import BaseMode
from cvp.config.sections.appearance import AppMode
from cvp.containers.immutable_list import ImmutableList
from cvp.imgui.begin import begin_context
from cvp.imgui.begin_child import begin_child_context
from cvp.imgui.button import button
from cvp.imgui.flags import color_var
from cvp.imgui.flags.child import BORDERS, RESIZE_X
from cvp.imgui.flags.input_text import READ_ONLY, InputTextFlags
from cvp.imgui.flags.style_var import StyleVar
from cvp.imgui.flags.window import ROOT_STATIC_VIEWPORT_FLAGS
from cvp.imgui.input_text_disabled import input_text_disabled
from cvp.imgui.push_style_var import (
    DEFAULT_DISABLE_BACKGROUND_COLOR,
    DEFAULT_DISABLE_TEXT_COLOR,
)
from cvp.imgui.set_next_window_as_viewport import set_next_window_as_viewport
from cvp.imgui.text_centered import text_centered
from cvp.imgui.theme import THEME_NAMES, apply_theme_with_name
from cvp.keyring.keyring import list_keyring_names, load_keyring, set_keyring
from cvp.logging.logging import logger
from cvp.msgs.msg import Msg
from cvp.renderer.context import RendererContext
from cvp.supabase.supabase import Supabase
from cvp.types.override import override
from cvp.variables import (
    DEFAULT_MAIN_LABEL,
    DEFAULT_MENU_LABEL,
    DEFAULT_MENU_WIDTH,
    FULL_SIZE,
    NOT_FOUND_INDEX,
)


class PreferenceMode(BaseMode):
    def __init__(self, context: RendererContext):
        super().__init__(context)
        self._theme_names = ImmutableList(THEME_NAMES)
        self._keyring_names = ImmutableList(list_keyring_names())
        self._menus = self._create_menus()
        self._show_server_supabase_key = False
        self._show_server_password = False

        self._error_color = 1.0, 0.0, 0.0, 1.0
        self._disable_text_color = DEFAULT_DISABLE_TEXT_COLOR
        self._disable_background_color = DEFAULT_DISABLE_BACKGROUND_COLOR
        self._supabase_client_runner = self.context.pm.create_thread_runner(
            self.on_supabase_client_main,
        )

    def on_supabase_client_main(self, supabase_url: str, supabase_key: str) -> None:
        self.context.supabase.create_client(supabase_url, supabase_key)

    def _create_menus(self) -> OrderedDict[str, Callable[[], None]]:
        result = OrderedDict()
        result["Appearance"] = self.on_appearance
        result["Chat"] = self.on_chat
        result["Keyring"] = self.on_keyring
        result["Server"] = self.on_server
        return result

    @staticmethod
    @override
    def get_mode() -> AppMode:
        return AppMode.preference

    @override
    def on_main_menu(self) -> None:
        pass

    @override
    def do_event(self, event: Event) -> bool:
        return False

    @override
    def do_msg(self, msg: Msg) -> bool:
        return False

    @override
    def on_keyboard(self, keys: ScancodeWrapper) -> None:
        pass

    @property
    def keyrings(self):
        return self.context.home.keyrings

    @property
    def selected(self) -> str:
        return self.context.config.preference_manager.selected

    @selected.setter
    def selected(self, value: str) -> None:
        self.context.config.preference_manager.selected = value

    @override
    def do_process(self) -> None:
        imgui.push_style_var(StyleVar.window_border_size, 0)
        try:
            set_next_window_as_viewport()
            with begin_context(type(self).__name__, flags=ROOT_STATIC_VIEWPORT_FLAGS):
                self.do_child_process()
        finally:
            imgui.pop_style_var()

    def do_child_process(
        self,
        menu_label=DEFAULT_MENU_LABEL,
        main_label=DEFAULT_MAIN_LABEL,
        split_x=DEFAULT_MENU_WIDTH,
    ):
        with begin_child_context(menu_label, split_x, child_flags=RESIZE_X | BORDERS):
            if imgui.begin_list_box("###MenuList", FULL_SIZE):
                try:
                    for key in self._menus.keys():
                        if imgui.selectable(key, key == self.selected)[1]:
                            self.selected = key
                finally:
                    imgui.end_list_box()

        imgui.same_line()

        with begin_child_context(main_label):
            if main_callback := self._menus.get(self.selected):
                imgui.text(self.selected)
                imgui.separator()

                main_callback()
            else:
                text_centered("Please select a item")

    # ----------------------------------------------------------------------------------
    # [Appearance] ---------------------------------------------------------------------

    @property
    def appearance_theme(self) -> str:
        return self.context.config.appearance.theme

    @appearance_theme.setter
    def appearance_theme(self, value: str) -> None:
        self.context.config.appearance.theme = value

    @property
    def theme_index(self) -> int:
        try:
            return self._theme_names.index(self.appearance_theme)
        except ValueError:
            return NOT_FOUND_INDEX

    def on_appearance(self) -> None:
        theme_result = imgui.combo("Theme", self.theme_index, self._theme_names)
        theme_changed, theme_index = theme_result
        assert isinstance(theme_changed, bool)
        assert isinstance(theme_index, int)

        if theme_changed and 0 <= theme_index < len(self._theme_names):
            try:
                theme_name = self._theme_names[theme_index]
                apply_theme_with_name(theme_name)
            except BaseException as e:
                logger.error(f"Changed theme error: {e}")
            else:
                logger.info(f"Changed theme: '{theme_name}'")
                self.appearance_theme = theme_name

        imgui.show_font_selector("Font")

    # ----------------------------------------------------------------------------------
    # [Chat] ---------------------------------------------------------------------------

    @property
    def chat_ollama_url(self) -> str:
        return self.context.config.chat.ollama_url

    @chat_ollama_url.setter
    def chat_ollama_url(self, value: str) -> None:
        self.context.config.chat.ollama_url = value

    def on_chat(self) -> None:
        self.chat_ollama_url = imgui.input_text("Ollama URL", self.chat_ollama_url)[1]

    # ----------------------------------------------------------------------------------
    # [Keyring] ------------------------------------------------------------------------

    @property
    def keyring_backend(self) -> str:
        return self.context.config.keyring.backend

    @keyring_backend.setter
    def keyring_backend(self, value: str) -> None:
        self.context.config.keyring.backend = value

    @property
    def keyring_backend_index(self) -> int:
        try:
            return self._keyring_names.index(self.keyring_backend)
        except ValueError:
            return NOT_FOUND_INDEX

    def on_keyring(self) -> None:
        backend_index = self.keyring_backend_index
        backend_result = imgui.combo("Backend", backend_index, self._keyring_names)
        backend_changed, backend_index = backend_result
        assert isinstance(backend_changed, bool)
        assert isinstance(backend_index, int)

        if backend_changed and 0 <= backend_index < len(self._keyring_names):
            try:
                backend_name = self._keyring_names[backend_index]
                set_keyring(load_keyring(backend_name))
            except BaseException as e:
                logger.error(f"Changed backend error: {e}")
            else:
                logger.info(f"Changed backend: '{backend_name}'")
                self.keyring_backend = backend_name

    # ----------------------------------------------------------------------------------
    # [Server] -------------------------------------------------------------------------

    @property
    def supabase_key_input_flags(self) -> int:
        flags = InputTextFlags.enter_returns_true
        if not self._show_server_supabase_key:
            flags |= InputTextFlags.password
        return int(flags)

    @property
    def password_input_flags(self) -> int:
        flags = InputTextFlags.enter_returns_true
        if not self._show_server_password:
            flags |= InputTextFlags.password
        return int(flags)

    @property
    def server_supabase_url(self) -> str:
        return self.context.config.server.supabase_url

    @server_supabase_url.setter
    def server_supabase_url(self, value: str) -> None:
        self.context.config.server.supabase_url = value

    @property
    def server_username(self) -> str:
        return self.context.config.server.username

    @server_username.setter
    def server_username(self, value: str) -> None:
        self.context.config.server.username = value

    def on_server(self) -> None:
        has_client = self.context.supabase.has_client
        supabase_client_running = self._supabase_client_runner.running
        has_supabase_client_error = bool(self._supabase_client_runner.error)
        disabled_create = supabase_client_running or has_client
        disabled_remove = supabase_client_running or not has_client
        read_only_flag = READ_ONLY if has_client else 0

        if has_client:
            imgui.push_style_color(color_var.TEXT, self._disable_text_color)
            imgui.push_style_color(color_var.FRAME_BG, self._disable_background_color)

        self.server_supabase_url = imgui.input_text(
            "Supabase URL",
            self.server_supabase_url,
            flags=read_only_flag,
        )[1]

        prev_supabase_key = self.keyrings.get_server_supabase_key(str())
        next_supabase_key = imgui.input_text(
            "Supabase Key",
            prev_supabase_key,
            flags=self.supabase_key_input_flags | read_only_flag,
        )[1]
        if prev_supabase_key != next_supabase_key:
            self.keyrings.set_server_supabase_key(next_supabase_key)

        if has_client:
            imgui.pop_style_color(2)

        show_supabase_key = imgui.checkbox(
            "Show Supabase Key",
            self._show_server_supabase_key,
        )
        show_supabase_key_changed = show_supabase_key[0]
        show_supabase_key_value = show_supabase_key[1]
        assert isinstance(show_supabase_key_changed, bool)
        assert isinstance(show_supabase_key_value, bool)
        if show_supabase_key_changed:
            self._show_server_supabase_key = show_supabase_key_value

        if button("Create Supabase Client", disabled=disabled_create):
            assert not supabase_client_running
            self._supabase_client_runner(self.server_supabase_url, prev_supabase_key)

        imgui.same_line()
        if button("Remove Supabase Client", disabled=disabled_remove):
            assert has_client
            assert not supabase_client_running
            self.context.supabase.remove_client()

        if has_supabase_client_error:
            error_message = str(self._supabase_client_runner.error)
            imgui.text_colored(self._error_color, error_message)

        if not has_client:
            return

        imgui.separator()

        has_session = self.context.supabase.has_session
        self.server_username = imgui.input_text("Username", self.server_username)[1]

        prev_password = self.keyrings.get_server_password(str())
        next_password = imgui.input_text(
            "Password",
            prev_password,
            self.password_input_flags,
        )[1]
        if prev_password != next_password:
            self.keyrings.set_server_password(next_password)

        show_password = imgui.checkbox("Show Password", self._show_server_password)
        show_password_changed = show_password[0]
        show_password_value = show_password[1]
        assert isinstance(show_password_changed, bool)
        assert isinstance(show_password_value, bool)
        if show_password_changed:
            self._show_server_password = show_password_value

        # self.context.supabase.login(
        #     self.server_supabase_url,
        #     next_supabase_key,
        #     self.server_username,
        #     next_password,
        # )
