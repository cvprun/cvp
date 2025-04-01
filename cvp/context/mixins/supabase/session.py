# -*- coding: utf-8 -*-

from typing import Final, NamedTuple

from cvp.concurrency.threading.runnable import ThreadRunnable
from cvp.context.mixins._base import BaseContextMixin


class _SupabaseSessionStatus(NamedTuple):
    has_session: bool
    has_error: bool
    error_message: str
    running: bool
    disabled_create: bool
    disabled_remove: bool


_SessionThreadRunner = ThreadRunnable[[str, str], None]


class SupabaseSessionMixin(BaseContextMixin):
    _create_supabase_session_runner: _SessionThreadRunner

    def _on_supabase_session_main(self, username: str, password: str) -> None:
        self._supabase.sign_in_with_password(username, password)

    @property
    def server_username(self) -> str:
        return self._config.server.username

    @server_username.setter
    def server_username(self, value: str) -> None:
        self._config.server.username = value

    __supabase_password__: Final[str] = "password"

    @property
    def server_password(self) -> str:
        return self._keyring.supabase.get_or_empty(self.__supabase_password__)

    @server_password.setter
    def server_password(self, value: str) -> None:
        self._keyring.supabase.set(self.__supabase_password__, value)

    def get_supabase_session_status(self):
        has_session = self._supabase.has_session
        has_error = bool(self._create_supabase_session_runner.error)
        error_message = str(self._create_supabase_session_runner.error)
        running = self._create_supabase_session_runner.running
        disabled_create = running or has_session
        disabled_remove = running or not has_session

        return _SupabaseSessionStatus(
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
        if self._create_supabase_session_runner.running:
            raise ValueError("The supabase session creation runner is running")

        self._create_supabase_session_runner(supabase_url, supabase_key)

    def remove_supabase_session(self) -> None:
        if not self._supabase.has_session:
            raise ValueError("The Supabase session is not created")
        if self._create_supabase_session_runner.running:
            raise ValueError("The supabase session creation runner is running")
        self._supabase.remove_first_session()
