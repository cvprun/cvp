# -*- coding: utf-8 -*-

from gotrue import User
from imgui_bundle import imgui, imspinner

from cvp.apps.player.modes.preference._base import BasePreference
from cvp.imgui.button import button
from cvp.imgui.flags import color_var
from cvp.imgui.flags.input_text import READ_ONLY, InputTextFlags
from cvp.imgui.input_text_value import input_text_value
from cvp.renderer.context import Context
from cvp.types.override import override


class Supabase(BasePreference):
    def __init__(self, context: Context):
        super().__init__(context)
        self._show_supabase_key = False
        self._show_password = False

    @property
    def keyrings(self):
        return self.context.home.keyrings

    @property
    def supabase_key_input_flags(self) -> int:
        flags = InputTextFlags.enter_returns_true
        if not self._show_supabase_key:
            flags |= InputTextFlags.password
        return int(flags)

    @property
    def supabase_url(self) -> str:
        return self.context.supabase_url

    @supabase_url.setter
    def supabase_url(self, value: str) -> None:
        self.context.supabase_url = value

    @property
    def supabase_key(self) -> str:
        return self.context.supabase_key

    @supabase_key.setter
    def supabase_key(self, value: str) -> None:
        self.context.supabase_key = value

    @property
    def password_input_flags(self) -> int:
        flags = InputTextFlags.enter_returns_true
        if not self._show_password:
            flags |= InputTextFlags.password
        return int(flags)

    @property
    def server_username(self) -> str:
        return self.context.server_username

    @server_username.setter
    def server_username(self, value: str) -> None:
        self.context.server_username = value

    @property
    def server_password(self) -> str:
        return self.context.server_password

    @server_password.setter
    def server_password(self, value: str) -> None:
        self.context.server_password = value

    @staticmethod
    def spinner(label: str):
        arc_radius = imgui.get_font_size() / 2.0
        imspinner.spinner_arc_rotation(label, arc_radius, 2.0, arcs=2)

    @staticmethod
    def push_disable_style() -> None:
        text_disabled = imgui.get_style_color_vec4(color_var.TEXT_DISABLED)
        imgui.push_style_color(color_var.TEXT, text_disabled)

        child_bg = imgui.get_style_color_vec4(color_var.CHILD_BG)
        imgui.push_style_color(color_var.FRAME_BG, child_bg)

    @staticmethod
    def pop_disable_style() -> None:
        imgui.pop_style_color(2)

    @override
    def do_process(self) -> None:
        client_status = self.context.get_supabase_client_status()
        self.do_client_process(
            has_client=client_status.has_client,
            has_error=client_status.has_error,
            error_message=client_status.error_message,
            running=client_status.running,
            disabled_create=client_status.disabled_create,
            disabled_remove=client_status.disabled_remove,
        )

        if client_status.running:
            return
        if not self.context.supabase.has_client:
            # Users can also remove client.
            return

        imgui.separator()

        session_status = self.context.get_supabase_session_status()
        self.do_login_process(
            has_session=session_status.has_session,
            has_error=session_status.has_error,
            error_message=session_status.error_message,
            running=session_status.running,
            disabled_create=session_status.disabled_create,
            disabled_remove=session_status.disabled_remove,
        )

        if session_status.running:
            return
        if not self.context.supabase.has_session:
            # Users can also remove sessions.
            return

        user = self.context.supabase.user
        if user is None:
            return

        imgui.separator()
        self.do_user_info_process(user)

    def do_client_process(
        self,
        has_client: bool,
        has_error: bool,
        error_message: str,
        running: bool,
        disabled_create: bool,
        disabled_remove: bool,
    ) -> None:
        read_only_flag = READ_ONLY if has_client else 0

        if has_client:
            self.push_disable_style()

        self.supabase_url = input_text_value(
            "Supabase URL",
            self.supabase_url,
            read_only_flag,
        )

        prev_supabase_key = self.supabase_key
        next_supabase_key = input_text_value(
            "Supabase Key",
            prev_supabase_key,
            self.supabase_key_input_flags | read_only_flag,
        )
        if prev_supabase_key != next_supabase_key:
            self.supabase_key = next_supabase_key

        if has_client:
            self.pop_disable_style()

        show_supabase_key = imgui.checkbox("Show Supabase Key", self._show_supabase_key)
        show_supabase_key_changed = show_supabase_key[0]
        show_supabase_key_value = show_supabase_key[1]
        assert isinstance(show_supabase_key_changed, bool)
        assert isinstance(show_supabase_key_value, bool)
        if show_supabase_key_changed:
            self._show_supabase_key = show_supabase_key_value

        if button("Create client", disabled=disabled_create):
            self.context.create_supabase_client(
                self.supabase_url,
                prev_supabase_key,
            )
        imgui.same_line()
        if button("Remove client", disabled=disabled_remove):
            self.context.remove_supabase_client()

        if running:
            imgui.same_line()
            self.spinner("Create client running")

        if has_error:
            imgui.text_colored(self.context.error_color, error_message)

    def do_login_process(
        self,
        has_session: bool,
        has_error: bool,
        error_message: str,
        running: bool,
        disabled_create: bool,
        disabled_remove: bool,
    ) -> None:
        read_only_flag = READ_ONLY if has_session else 0

        if has_session:
            self.push_disable_style()

        self.server_username = input_text_value(
            "Username",
            self.server_username,
            read_only_flag,
        )

        prev_server_password = self.server_password
        next_server_password = input_text_value(
            "Password",
            prev_server_password,
            self.password_input_flags | read_only_flag,
        )
        if prev_server_password != next_server_password:
            self.server_password = next_server_password

        if has_session:
            self.pop_disable_style()

        show_password = imgui.checkbox("Show Password", self._show_password)
        show_password_changed = show_password[0]
        show_password_value = show_password[1]
        assert isinstance(show_password_changed, bool)
        assert isinstance(show_password_value, bool)
        if show_password_changed:
            self._show_password = show_password_value

        if button("Login", disabled=disabled_create):
            self.context.create_supabase_session(
                self.server_username,
                prev_server_password,
            )
        imgui.same_line()
        if button("Force remove session", disabled=disabled_remove):
            self.context.remove_supabase_session()

        if running:
            imgui.same_line()
            self.spinner("Create session running")

        if has_error:
            imgui.text_colored(self.context.error_color, error_message)

    def do_user_info_process(self, user: User) -> None:
        self.push_disable_style()
        try:
            imgui.input_text("Email", str(user.email))
            imgui.input_text("Phone", str(user.phone))
            imgui.input_text("Created At", user.created_at.isoformat())

            confirmed_at = user.confirmed_at.isoformat() if user.confirmed_at else str()
            imgui.input_text("Confirmed At", confirmed_at)

            e_confirmed_at = user.email_confirmed_at
            email_confirmed_at = e_confirmed_at.isoformat() if e_confirmed_at else str()
            imgui.input_text("Email Confirmed At", email_confirmed_at)

            p_confirmed_at = user.phone_confirmed_at
            phone_confirmed_at = p_confirmed_at.isoformat() if p_confirmed_at else str()
            imgui.input_text("Phone Confirmed At", phone_confirmed_at)

            l_sign_in_at = user.last_sign_in_at
            last_sign_in_at = l_sign_in_at.isoformat() if l_sign_in_at else str()
            imgui.input_text("Last Sign In At", last_sign_in_at)

            imgui.input_text("Role", str(user.role))

            updated_at = user.updated_at.isoformat() if user.updated_at else str()
            imgui.input_text("Updated At", updated_at)

            imgui.input_text("Is Anonymous", str(user.is_anonymous))
        finally:
            self.pop_disable_style()
