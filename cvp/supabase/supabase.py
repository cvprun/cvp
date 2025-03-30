# -*- coding: utf-8 -*-

from typing import Optional

from supabase import Client, create_client


class Supabase:
    _client: Optional[Client]

    def __init__(self):
        self._client = None

    @property
    def has_client(self) -> bool:
        return self._client is not None

    def create_client(
        self,
        supabase_url: str,
        supabase_key: str,
    ) -> bool:
        try:
            self._client = create_client(supabase_url, supabase_key)
        except:  # noqa
            self._client = None
            raise
        return self._client is not None

    def remove_client(self) -> None:
        if self._client is not None:
            try:
                self._client.remove_all_channels()
            except NotImplementedError:
                pass
        self._client = None

    @property
    def has_session(self) -> bool:
        if self._client is None:
            return False

        return True

    def login(
        self,
        supabase_url: str,
        supabase_key: str,
        username: str,
        password: str,
    ) -> bool:
        self._client = create_client(supabase_url, supabase_key)
        return False

    def logout(self) -> None:
        pass
