# -*- coding: utf-8 -*-

from datetime import UTC, datetime
from typing import Dict, List, Optional, Union

from cvp.chat.cache import Cache
from cvp.chat.conversation import ChatConversation
from cvp.chat.database import ChatDatabase
from cvp.chat.message import ChatMessage
from cvp.resources.subdirs.chat import ChatPath
from cvp.variables import DEFAULT_CHAT_LIMIT


class ChatManager:
    _caches: Dict[int, Cache]

    def __init__(
        self,
        path: ChatPath,
        limit=DEFAULT_CHAT_LIMIT,
        *,
        create_tables=False,
        reload=False,
    ):
        self._limit = limit
        self._caches = dict()
        self._database = ChatDatabase(
            path=path.get_database_path(),
            create_tables=create_tables,
        )
        if reload:
            self.reload_conversations()

    def reload_conversations(self) -> None:
        conv_rows = self._database.select_conversation_latest(limit=self._limit)
        self._caches.update({conv.id: Cache(conv) for conv in conv_rows})

    def conversation_labels(self) -> List[str]:
        return list(c.label for c in self._caches.values())

    def create_new_chat(
        self,
        title: Optional[str] = None,
        request: Optional[str] = None,
        response: Optional[str] = None,
        error: Optional[str] = None,
        created_at: Optional[Union[datetime, str]] = None,
    ) -> Cache:
        if title is None:
            title = str()
        assert isinstance(title, str)

        if created_at is None:
            created_at = datetime.now(UTC).isoformat()
        elif isinstance(created_at, datetime):
            created_at = created_at.astimezone(UTC).isoformat()
        assert isinstance(created_at, str)

        conv_id, msg_id = self._database.insert_conversation_and_message(
            title, request, response, error, created_at
        )

        conv_row = conv_id, title, created_at, None
        conv = ChatConversation.from_row(conv_row)

        msg_row = msg_id, conv_id, request, response, error, created_at
        msg = ChatMessage.from_row(msg_row)

        assert conv_id not in self._caches
        cache = Cache(conv, (msg,))
        self._caches[conv_id] = cache
        return cache

    def append_chat(
        self,
        conversation_id: int,
        request: Optional[str] = None,
        response: Optional[str] = None,
        error: Optional[str] = None,
        created_at: Optional[Union[datetime, str]] = None,
    ) -> ChatMessage:
        if created_at is None:
            created_at = datetime.now(UTC).isoformat()
        elif isinstance(created_at, datetime):
            created_at = created_at.astimezone(UTC).isoformat()
        assert isinstance(created_at, str)

        message_id = self._database.insert_message(
            conversation_id, request, response, error, created_at
        )
        message_row = message_id, conversation_id, request, response, error, created_at
        message = ChatMessage.from_row(message_row)

        assert conversation_id in self._caches
        cache = self._caches[conversation_id]
        if cache.messages is None:
            old_messages = self._database.select_message_latest_after_id(
                conversation_id,
                limit=self._limit,
            )
            cache.appendleft_messages(*old_messages)
        cache.appendleft_messages(message)
        return message

    def messages(self, conversation_id: int) -> List[ChatMessage]:
        assert conversation_id in self._caches
        cache = self._caches[conversation_id]
        if cache.messages is None:
            messages = self._database.select_message_latest_after_id(
                conversation_id,
                limit=self._limit,
            )
            cache.appendleft_messages(*messages)
        assert cache.messages is not None
        return list(cache.messages)
