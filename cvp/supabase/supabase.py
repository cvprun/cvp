# -*- coding: utf-8 -*-

from typing import Optional

from gotrue import AuthResponse, User

from supabase import Client, create_client


class Supabase:
    _client: Optional[Client]
    _first_session: Optional[AuthResponse]

    def __init__(self):
        self._client = None
        self._first_session = None

    @property
    def has_client(self) -> bool:
        return self._client is not None

    def create_client(self, supabase_url: str, supabase_key: str) -> bool:
        try:
            self._client = create_client(supabase_url, supabase_key)
        except:  # noqa
            self._client = None
            raise
        finally:
            self._first_session = None
        return self._client is not None

    def remove_client(self) -> None:
        if self._client is not None:
            try:
                self._client.remove_all_channels()
            except NotImplementedError:
                pass
        self._client = None

    @property
    def client(self):
        if self._client is None:
            raise ValueError("Supabase client is not initialized")
        return self._client

    @property
    def auth(self):
        return self.client.auth

    @property
    def has_session(self) -> bool:
        return self._first_session is not None

    def sign_in_with_password(self, email: str, password: str) -> bool:
        credentials = {"email": email, "password": password}
        try:
            self._first_session = self.auth.sign_in_with_password(credentials)
        except:  # noqa
            self._first_session = None
            raise
        return self._first_session is not None

    def sign_out(self) -> None:
        try:
            self.auth.sign_out()
        finally:
            self._first_session = None

    def remove_first_session(self) -> None:
        self._first_session = None

    @property
    def first_session(self):
        if self._first_session is None:
            raise ValueError("Supabase session is not initialized")
        return self._first_session

    @property
    def user(self) -> Optional[User]:
        return self.first_session.user
