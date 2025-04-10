# -*- coding: utf-8 -*-

import sqlite3
from os import PathLike
from pathlib import Path
from typing import List, Optional, Tuple

from cvp.chat import queries
from cvp.chat.conversation import ChatConversation
from cvp.chat.message import ChatMessage
from cvp.chat.stream import ChatStream
from cvp.chrono.isoformat import DateTimeLike, isoformat_with_utc
from cvp.variables import DEFAULT_CHAT_LIMIT


class ChatDatabase:
    def __init__(self, path: PathLike[str], *, create_tables=False):
        self._path = Path(path)
        if create_tables:
            self.create_tables()

    @property
    def path(self):
        return self._path

    def connect(self):
        return sqlite3.connect(self._path)

    def create_tables(self):
        with self.connect() as conn:
            conn.execute(queries.CREATE_TABLE_CONVERSATION)
            conn.execute(queries.CREATE_TABLE_MESSAGE)
            conn.execute(queries.CREATE_TABLE_STREAM)

    # ----------------------------------------------------------------------------------
    # [conversation] -------------------------------------------------------------------

    @staticmethod
    def _insert_conversation(
        conn: sqlite3.Connection,
        title: str,
        created_at: str,
    ) -> int:
        query = queries.INSERT_CONVERSATION
        parameters = (title, created_at)
        conversation_id = conn.execute(query, parameters).lastrowid
        assert conversation_id is not None
        return conversation_id

    def insert_conversation(self, title: str, created_at: DateTimeLike = None) -> int:
        created_at = isoformat_with_utc(created_at)
        assert isinstance(created_at, str)
        with self.connect() as conn:
            return self._insert_conversation(conn, title, created_at)

    def update_conversation_title(
        self,
        id_: int,
        title: str,
        updated_at: DateTimeLike = None,
    ) -> None:
        updated_at = isoformat_with_utc(updated_at)
        assert isinstance(updated_at, str)

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

    @staticmethod
    def _insert_message(
        conn: sqlite3.Connection,
        conversation_id: int,
        request: str,
        error: str,
        status: int,
        created_at: str,
    ) -> int:
        query = queries.INSERT_MESSAGE
        parameters = (conversation_id, request, error, status, created_at)
        message_id = conn.execute(query, parameters).lastrowid
        assert message_id is not None
        return message_id

    def insert_message(
        self,
        conversation_id: int,
        request: str,
        error: str,
        status=0,
        created_at: DateTimeLike = None,
    ) -> int:
        created_at = isoformat_with_utc(created_at)
        assert isinstance(created_at, str)

        with self.connect() as conn:
            return self._insert_message(
                conn,
                conversation_id,
                request,
                error,
                status,
                created_at,
            )

    def update_message_error_and_status(
        self,
        id_: int,
        error: Optional[str] = None,
        status=0,
        updated_at: DateTimeLike = None,
    ) -> None:
        updated_at = isoformat_with_utc(updated_at)
        assert isinstance(updated_at, str)

        with self.connect() as conn:
            query = queries.UPDATE_MESSAGE_ERROR_STATUS
            parameters = (error, status, updated_at, id_)
            conn.execute(query, parameters)

    def delete_message(self, id_: int) -> None:
        with self.connect() as conn:
            query = queries.DELETE_MESSAGE
            parameters = (id_,)
            conn.execute(query, parameters)

    def select_message(self, conversation_id: int) -> List[ChatMessage]:
        with self.connect() as conn:
            query = queries.SELECT_MESSAGE
            parameters = (conversation_id,)
            result = list()
            for row in conn.execute(query, parameters):
                result.append(ChatMessage.from_row(row))
            return result

    # ----------------------------------------------------------------------------------
    # [stream] -------------------------------------------------------------------------

    def insert_stream(
        self,
        message_id: int,
        chunk: Optional[str] = None,
        created_at: DateTimeLike = None,
    ) -> int:
        created_at = isoformat_with_utc(created_at)
        assert isinstance(created_at, str)

        with self.connect() as conn:
            query = queries.INSERT_STREAM
            parameters = (message_id, chunk, created_at)
            stream_id = conn.execute(query, parameters).lastrowid
            assert stream_id is not None
            return stream_id

    def delete_stream(self, id_: int) -> None:
        with self.connect() as conn:
            query = queries.DELETE_STREAM
            parameters = (id_,)
            conn.execute(query, parameters)

    def select_stream(self, message_id: int) -> List[ChatStream]:
        with self.connect() as conn:
            query = queries.SELECT_STREAM
            parameters = (message_id,)
            result = list()
            for row in conn.execute(query, parameters):
                result.append(ChatStream.from_row(row))
            return result

    # ----------------------------------------------------------------------------------
    # [conversation + message] ---------------------------------------------------------

    def insert_conversation_and_message(
        self,
        title: str,
        request: str,
        created_at: DateTimeLike = None,
    ) -> Tuple[int, int]:
        created_at = isoformat_with_utc(created_at)
        assert isinstance(created_at, str)

        with self.connect() as conn:
            conv_id = self._insert_conversation(conn, title, created_at)
            msg_id = self._insert_message(conn, conv_id, request, str(), 0, created_at)
            assert conv_id is not None
            assert msg_id is not None
            return conv_id, msg_id
