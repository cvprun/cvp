# -*- coding: utf-8 -*-

import sqlite3
from typing import Optional

from cvp.chat import queries
from cvp.chrono.tznow import tznow
from cvp.resources.home import HomeDir
from cvp.variables import DEFAULT_CHAT_LIMIT


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

    def insert_conversation(self, title: Optional[str] = None) -> Optional[int]:
        if title is None:
            title = str()
        assert isinstance(title, str)
        with self.connect() as conn:
            query = queries.INSERT_CONVERSATION
            parameters = (title, tznow().isoformat())
            return conn.execute(query, parameters).lastrowid

    def update_conversation_title(self, id_: int, title: str) -> None:
        with self.connect() as conn:
            query = queries.UPDATE_CONVERSATION_TITLE
            parameters = (title, id_)
            conn.execute(query, parameters)

    def delete_conversation(self, id_: int) -> None:
        with self.connect() as conn:
            query = queries.DELETE_CONVERSATION
            parameters = (id_,)
            conn.execute(query, parameters)

    def select_conversation_latest(self, limit=DEFAULT_CHAT_LIMIT):
        with self.connect() as conn:
            query = queries.SELECT_CONVERSATION_LATEST
            parameters = (limit,)
            for row in conn.execute(query, parameters):
                assert isinstance(row, tuple)
                print(row)

    def select_conversation_latest_after_id(self, id_: int, limit=DEFAULT_CHAT_LIMIT):
        with self.connect() as conn:
            query = queries.SELECT_CONVERSATION_LATEST_AFTER_ID
            parameters = id_, limit
            for row in conn.execute(query, parameters):
                print(row)

    # ----------------------------------------------------------------------------------
    # [message] ------------------------------------------------------------------------
