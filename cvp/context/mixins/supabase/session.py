# -*- coding: utf-8 -*-

from typing import NamedTuple

from cvp.context.mixins._base import BaseContextMixin
from cvp.keyring.keys import SupabaseKey


class SupabaseSessionMixin(BaseContextMixin):
    @property
    def _supabase_session_runner(self):
        return self.get_process_runner(self.__on_supabase_session_main)

    def __on_supabase_session_main(self, username: str, password: str) -> None:
        self._supabase.sign_in_with_password(username, password)

    @property
    def server_username(self) -> str:
        return self._config.server.username

    @server_username.setter
    def server_username(self, value: str) -> None:
        self._config.server.username = value

    @property
    def server_password(self) -> str:
        return self._keyring.supabase.get_or_empty(SupabaseKey.password)

    @server_password.setter
    def server_password(self, value: str) -> None:
        self._keyring.supabase.set(SupabaseKey.password, value)

    class _SupabaseSessionStatus(NamedTuple):
        has_session: bool
        has_error: bool
        error_message: str
        running: bool
        disabled_create: bool
        disabled_remove: bool

    def get_supabase_session_status(self):
        has_session = self._supabase.has_session
        has_error = bool(self._supabase_session_runner.error)
        error_message = str(self._supabase_session_runner.error)
        running = self._supabase_session_runner.running
        disabled_create = running or has_session
        disabled_remove = running or not has_session

        return self._SupabaseSessionStatus(
            has_session=has_session,
            has_error=has_error,
            error_message=error_message,
            running=running,
            disabled_create=disabled_create,
            disabled_remove=disabled_remove,
        )

    def create_supabase_session(self, supabase_url: str, supabase_key: str) -> None:
        if self._supabase.has_session:
            raise ValueError("The Supabase session is already created")
        if self._supabase_session_runner.running:
            raise ValueError("The supabase session creation runner is running")

        self._supabase_session_runner(supabase_url, supabase_key)

    def remove_supabase_session(self) -> None:
        if not self._supabase.has_session:
            raise ValueError("The Supabase session is not created")
        if self._supabase_session_runner.running:
            raise ValueError("The supabase session creation runner is running")
        self._supabase.remove_first_session()
