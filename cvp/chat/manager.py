# -*- coding: utf-8 -*-

import sqlite3
from dataclasses import dataclass
from datetime import UTC, datetime
from typing import List, Optional

from cvp.chat import queries
from cvp.resources.home import HomeDir
from cvp.variables import DEFAULT_CHAT_LIMIT


@dataclass
class ChatConversation:
    id: int
    title: str
    created_at: datetime
    updated_at: Optional[datetime] = None

    @classmethod
    def from_row(cls, row):
        assert isinstance(row, tuple)
        assert 4 == len(row)
        id_, title, created_at, updated_at = row
        assert isinstance(id_, int)
        assert isinstance(title, str)
        assert isinstance(created_at, str)
        assert isinstance(updated_at, (type(None), str))
        return cls(
            id_,
            title,
            datetime.fromisoformat(created_at),
            datetime.fromisoformat(updated_at) if updated_at else None,
        )


@dataclass
class ChatMessage:
    id: int
    conversation_id: int
    request: Optional[str]
    response: Optional[str]
    error: Optional[str]
    created_at: datetime

    @classmethod
    def from_row(cls, row):
        assert isinstance(row, tuple)
        assert 6 == len(row)
        id_, conversation_id, request, response, error, created_at = row
        assert isinstance(id_, int)
        assert isinstance(conversation_id, int)
        assert isinstance(request, (type(None), str))
        assert isinstance(response, (type(None), str))
        assert isinstance(error, (type(None), str))
        assert isinstance(created_at, str)
        return cls(
            id_,
            conversation_id,
            request,
            response,
            error,
            datetime.fromisoformat(created_at),
        )


class ChatManager:
    def __init__(self, home: HomeDir, *, create_tables=False):
        super().__init__()
        self._path = home.chat

        if create_tables:
            self.create_tables()

    @property
    def path(self):
        return self._path

    @property
    def database_path(self):
        return self._path.get_database_path()

    def connect(self):
        return sqlite3.connect(self.database_path)

    def create_tables(self):
        with self.connect() as conn:
            conn.execute(queries.CREATE_TABLE_CONVERSATION)
            conn.execute(queries.CREATE_TABLE_MESSAGE)

    # ----------------------------------------------------------------------------------
    # [conversation] -------------------------------------------------------------------

    def insert_conversation(
        self,
        title: Optional[str] = None,
        created_at: Optional[datetime] = None,
    ) -> Optional[int]:
        if title is None:
            title = str()
        if created_at is None:
            created_at = datetime.now(UTC).isoformat()
        assert isinstance(title, str)
        assert isinstance(created_at, str)

        with self.connect() as conn:
            query = queries.INSERT_CONVERSATION
            parameters = (title, created_at)
            return conn.execute(query, parameters).lastrowid

    def update_conversation_title(
        self,
        id_: int,
        title: str,
        updated_at: Optional[datetime] = None,
    ) -> None:
        if updated_at is None:
            updated_at = datetime.now(UTC).isoformat()
        assert isinstance(updated_at, datetime)

        with self.connect() as conn:
            query = queries.UPDATE_CONVERSATION_TITLE
            parameters = (title, updated_at, id_)
            conn.execute(query, parameters)

    def delete_conversation(self, id_: int) -> None:
        with self.connect() as conn:
            query = queries.DELETE_CONVERSATION
            parameters = (id_,)
            conn.execute(query, parameters)

    def select_conversation_latest(
        self,
        limit=DEFAULT_CHAT_LIMIT,
    ) -> List[ChatConversation]:
        with self.connect() as conn:
            query = queries.SELECT_CONVERSATION_LATEST
            parameters = (limit,)
            result = list()
            for row in conn.execute(query, parameters):
                result.append(ChatConversation.from_row(row))
            return result

    def select_conversation_latest_after_id(self, id_: int, limit=DEFAULT_CHAT_LIMIT):
        with self.connect() as conn:
            query = queries.SELECT_CONVERSATION_LATEST_AFTER_ID
            parameters = id_, limit
            result = list()
            for row in conn.execute(query, parameters):
                result.append(ChatConversation.from_row(row))
            return result

    # ----------------------------------------------------------------------------------
    # [message] ------------------------------------------------------------------------

    def insert_message(
        self,
        conversation_id: int,
        request: Optional[str] = None,
        response: Optional[str] = None,
        error: Optional[str] = None,
        created_at: Optional[datetime] = None,
    ) -> Optional[int]:
        if created_at is None:
            created_at = datetime.now(UTC).isoformat()
        assert isinstance(created_at, str)

        with self.connect() as conn:
            query = queries.INSERT_MESSAGE
            parameters = (conversation_id, request, response, error, created_at)
            return conn.execute(query, parameters).lastrowid

    def delete_message(self, id_: int) -> None:
        with self.connect() as conn:
            query = queries.DELETE_MESSAGE
            parameters = (id_,)
            conn.execute(query, parameters)

    def select_message_latest(
        self,
        limit=DEFAULT_CHAT_LIMIT,
    ) -> List[ChatMessage]:
        with self.connect() as conn:
            query = queries.SELECT_MESSAGE_LATEST
            parameters = (limit,)
            result = list()
            for row in conn.execute(query, parameters):
                result.append(ChatMessage.from_row(row))
            return result

    def select_message_latest_after_id(self, id_: int, limit=DEFAULT_CHAT_LIMIT):
        with self.connect() as conn:
            query = queries.SELECT_MESSAGE_LATEST_AFTER_ID
            parameters = id_, limit
            result = list()
            for row in conn.execute(query, parameters):
                result.append(ChatMessage.from_row(row))
            return result
