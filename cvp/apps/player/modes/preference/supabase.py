# -*- coding: utf-8 -*-

from datetime import datetime

from gotrue import User
from imgui_bundle import imgui

from cvp.apps.player.modes.preference._base import BasePreference
from cvp.imgui.button import button
from cvp.imgui.checkbox import checkbox
from cvp.imgui.flags.input_text import READ_ONLY, InputTextFlags
from cvp.imgui.input_text_value import input_text_value
from cvp.imgui.push_style_color import style_disable_input_context
from cvp.imgui.spinner import spinner
from cvp.renderer.context import Context
from cvp.types.override import override


class Supabase(BasePreference):
    def __init__(self, context: Context):
        super().__init__(context)
        self._show_supabase_key = False
        self._show_password = False

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
    def supabase_key_input_flags(self) -> int:
        flags = InputTextFlags.enter_returns_true
        if not self._show_supabase_key:
            flags |= InputTextFlags.password
        return int(flags)

    @property
    def username(self) -> str:
        return self.context.server_username

    @username.setter
    def username(self, value: str) -> None:
        self.context.server_username = value

    @property
    def password(self) -> str:
        return self.context.server_password

    @password.setter
    def password(self, value: str) -> None:
        self.context.server_password = value

    @property
    def password_input_flags(self) -> int:
        flags = InputTextFlags.enter_returns_true
        if not self._show_password:
            flags |= InputTextFlags.password
        return int(flags)

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
        with style_disable_input_context(cancel=not has_client):
            self.supabase_url = input_text_value(
                label="Supabase URL",
                value=self.supabase_url,
                flags=READ_ONLY if has_client else 0,
            )

            next_supabase_key = input_text_value(
                label="Supabase Key",
                value=self.supabase_key,
                flags=self.supabase_key_input_flags | (READ_ONLY if has_client else 0),
            )
            if self.supabase_key != next_supabase_key:
                self.supabase_key = next_supabase_key

        if check_result := checkbox("Show Supabase Key", self._show_supabase_key):
            self._show_supabase_key = check_result.state

        if button("Create client", disabled=disabled_create):
            self.context.create_supabase_client(self.supabase_url, self.supabase_key)
        imgui.same_line()
        if button("Remove client", disabled=disabled_remove):
            self.context.remove_supabase_client()

        if running:
            imgui.same_line()
            spinner("Create client running")

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
        with style_disable_input_context(cancel=not has_session):
            self.username = input_text_value(
                label="Username",
                value=self.username,
                flags=READ_ONLY if has_session else 0,
            )

            next_server_password = input_text_value(
                label="Password",
                value=self.password,
                flags=self.password_input_flags | (READ_ONLY if has_session else 0),
            )
            if self.password != next_server_password:
                self.password = next_server_password

        if check_result := checkbox("Show Password", self._show_password):
            self._show_password = check_result.state

        if button("Login", disabled=disabled_create):
            self.context.create_supabase_session(self.username, self.password)
        imgui.same_line()
        if button("Force remove session", disabled=disabled_remove):
            self.context.remove_supabase_session()

        if running:
            imgui.same_line()
            spinner("Create session running")

        if has_error:
            imgui.text_colored(self.context.error_color, error_message)

    def do_user_info_process(self, user: User) -> None:
        assert isinstance(user.id, str)
        # app_metadata: Dict[str, Any]
        # user_metadata: Dict[str, Any]
        assert isinstance(user.aud, str)
        # confirmation_sent_at: Optional[datetime] = None
        # recovery_sent_at: Optional[datetime] = None
        # email_change_sent_at: Optional[datetime] = None
        # new_email: Optional[str] = None
        # new_phone: Optional[str] = None
        # invited_at: Optional[datetime] = None
        # action_link: Optional[str] = None

        email = user.email if user.email else str()
        phone = user.phone if user.phone else str()

        assert isinstance(user.created_at, datetime)
        created_at = user.created_at.isoformat()

        confirmed_at = user.confirmed_at.isoformat() if user.confirmed_at else str()

        user_eca = user.email_confirmed_at
        email_confirmed_at = user_eca.isoformat() if user_eca else str()

        user_pca = user.phone_confirmed_at
        phone_confirmed_at = user_pca.isoformat() if user_pca else str()

        user_last = user.last_sign_in_at
        last_sign_in_at = user_last.isoformat() if user_last else str()

        role = user.role if user.role else str()
        updated_at = user.updated_at.isoformat() if user.updated_at else str()

        # identities: Optional[List[UserIdentity]] = None

        assert isinstance(user.is_anonymous, bool)
        is_anonymous = str(bool(user.is_anonymous))

        # factors: Optional[List[Factor]] = None

        with style_disable_input_context():
            imgui.input_text("ID", user.id)
            imgui.input_text("Audience", user.aud)
            imgui.input_text("Email", email)
            imgui.input_text("Phone", phone)
            imgui.input_text("Created At", created_at)
            imgui.input_text("Confirmed At", confirmed_at)
            imgui.input_text("Email Confirmed At", email_confirmed_at)
            imgui.input_text("Phone Confirmed At", phone_confirmed_at)
            imgui.input_text("Last Sign In At", last_sign_in_at)
            imgui.input_text("Role", role)
            imgui.input_text("Updated At", updated_at)
            imgui.input_text("Is Anonymous", is_anonymous)
