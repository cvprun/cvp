# -*- coding: utf-8 -*-

import sqlite3
from datetime import UTC, datetime
from os import PathLike
from pathlib import Path
from typing import List, Optional, Tuple, Union

from cvp.chat import queries
from cvp.chat.conversation import ChatConversation
from cvp.chat.message import ChatMessage
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

    # ----------------------------------------------------------------------------------
    # [conversation] -------------------------------------------------------------------

    def insert_conversation(
        self,
        title: Optional[str] = None,
        created_at: Optional[Union[datetime, str]] = None,
    ) -> int:
        if title is None:
            title = str()
        assert isinstance(title, str)

        if created_at is None:
            created_at = datetime.now(UTC).isoformat()
        elif isinstance(created_at, datetime):
            created_at = created_at.astimezone(UTC).isoformat()
        assert isinstance(created_at, str)

        with self.connect() as conn:
            query = queries.INSERT_CONVERSATION
            parameters = (title, created_at)
            conversation_id = conn.execute(query, parameters).lastrowid
            assert conversation_id is not None
            return conversation_id

    def update_conversation_title(
        self,
        id_: int,
        title: str,
        updated_at: Optional[Union[datetime, str]] = None,
    ) -> None:
        if updated_at is None:
            updated_at = datetime.now(UTC).isoformat()
        elif isinstance(updated_at, datetime):
            updated_at = updated_at.astimezone(UTC).isoformat()
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

    def insert_message(
        self,
        conversation_id: int,
        request: Optional[str] = None,
        response: Optional[str] = None,
        error: Optional[str] = None,
        created_at: Optional[Union[datetime, str]] = None,
    ) -> int:
        if created_at is None:
            created_at = datetime.now(UTC).isoformat()
        elif isinstance(created_at, datetime):
            created_at = created_at.astimezone(UTC).isoformat()
        assert isinstance(created_at, str)

        with self.connect() as conn:
            query = queries.INSERT_MESSAGE
            parameters = (conversation_id, request, response, error, created_at)
            message_id = conn.execute(query, parameters).lastrowid
            assert message_id is not None
            return message_id

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

    # ----------------------------------------------------------------------------------
    # [mixins] -------------------------------------------------------------------------

    def insert_conversation_and_message(
        self,
        title: Optional[str] = None,
        request: Optional[str] = None,
        response: Optional[str] = None,
        error: Optional[str] = None,
        created_at: Optional[Union[datetime, str]] = None,
    ) -> Tuple[int, int]:
        if title is None:
            title = str()
        assert isinstance(title, str)

        if created_at is None:
            created_at = datetime.now(UTC).isoformat()
        elif isinstance(created_at, datetime):
            created_at = created_at.astimezone(UTC).isoformat()
        assert isinstance(created_at, str)

        with self.connect() as conn:
            conv_query = queries.INSERT_CONVERSATION
            conv_parameters = (title, created_at)
            conversation_id = conn.execute(conv_query, conv_parameters).lastrowid

            msg_query = queries.INSERT_MESSAGE
            msg_parameters = (conversation_id, request, response, error, created_at)
            msg_id = conn.execute(msg_query, msg_parameters).lastrowid

            assert created_at is not None
            assert msg_id is not None

            return conversation_id, msg_id
