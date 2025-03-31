# -*- coding: utf-8 -*-

from typing import NamedTuple, Optional

from cvp.concurrency.threading.runnable import ThreadRunnable
from cvp.context.mixins._base import BaseContextMixin


class _SupabaseClientStatus(NamedTuple):
    has_client: bool
    has_error: bool
    error_message: str
    running: bool
    disabled_create: bool
    disabled_remove: bool


_ClientThreadRunner = ThreadRunnable[[str, str, Optional[str], Optional[str]], None]


class SupabaseClientMixin(BaseContextMixin):
    _create_supabase_client_runner: _ClientThreadRunner

    def _on_supabase_client_main(
        self,
        supabase_url: str,
        supabase_key: str,
        username: Optional[str] = None,
        password: Optional[str] = None,
    ) -> None:
        has_client = self._supabase.create_client(supabase_url, supabase_key)
        if not has_client:
            return

        if not username or not password:
            return

        assert self._supabase.has_client
        self._supabase.sign_in_with_password(username, password)

    @property
    def supabase_url(self) -> str:
        return self._config.server.supabase_url

    @supabase_url.setter
    def supabase_url(self, value: str) -> None:
        self._config.server.supabase_url = value

    @property
    def supabase_key(self) -> str:
        result = self._home.keyrings.get_server_supabase_key(str())
        assert result is not None
        return result

    @supabase_key.setter
    def supabase_key(self, value: str) -> None:
        self._home.keyrings.set_server_supabase_key(value)

    def get_supabase_client_status(self):
        has_client = self._supabase.has_client
        has_error = bool(self._create_supabase_client_runner.error)
        error_message = str(self._create_supabase_client_runner.error)
        running = self._create_supabase_client_runner.running
        disabled_create = running or has_client
        disabled_remove = running or not has_client

        return _SupabaseClientStatus(
            has_client=has_client,
            has_error=has_error,
            error_message=error_message,
            running=running,
            disabled_create=disabled_create,
            disabled_remove=disabled_remove,
        )

    def create_supabase_client(
        self,
        supabase_url: str,
        supabase_key: str,
        username: Optional[str] = None,
        password: Optional[str] = None,
    ) -> None:
        if self._supabase.has_client:
            raise ValueError("The Supabase client is already created")
        if self._create_supabase_client_runner.running:
            raise ValueError("The supabase client creation runner is running")

        self._create_supabase_client_runner(
            supabase_url,
            supabase_key,
            username,
            password,
        )

    def remove_supabase_client(self) -> None:
        if not self._supabase.has_client:
            raise ValueError("The Supabase client is not created")
        if self._create_supabase_client_runner.running:
            raise ValueError("The supabase client creation runner is running")
        self._supabase.remove_client()
