# -*- coding: utf-8 -*-

from datetime import UTC, datetime
from typing import Dict, List, Optional, Union

from cvp.chat.cache import ChatCache
from cvp.chat.conversation import ChatConversation
from cvp.chat.database import ChatDatabase
from cvp.chat.message import ChatMessage
from cvp.resources.subdirs.chat import ChatPath
from cvp.variables import DEFAULT_CHAT_LIMIT


class ChatManager:
    _caches: Dict[int, ChatCache]

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
        self._caches.update({conv.id: ChatCache(conv) for conv in conv_rows})

    def keys(self):
        return self._caches.keys()

    def values(self):
        return self._caches.values()

    def items(self):
        return self._caches.items()

    def __getitem__(self, conv_id: int):
        return self._caches[conv_id]

    def __setitem__(self, conv_id: int, value: ChatCache):
        self._caches[conv_id] = value

    def __delitem__(self, conv_id: int):
        del self._caches[conv_id]

    def create_new_chat(
        self,
        title: Optional[str] = None,
        request: Optional[str] = None,
        response: Optional[str] = None,
        error: Optional[str] = None,
        created_at: Optional[Union[datetime, str]] = None,
    ) -> ChatCache:
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
        cache = ChatCache(conv, (msg,))
        self._caches[conv_id] = cache
        return cache

    def refresh_messages(self, conversation_id: int, limit: Optional[int] = None):
        if conversation_id not in self._caches:
            raise KeyError(f"Not found conversation: {conversation_id}")

        if limit is None:
            limit = self._limit
        assert isinstance(limit, int)

        cache = self._caches[conversation_id]
        messages = self._database.select_message_latest_after_id(conversation_id, limit)
        cache.appendleft_messages(*messages)
        return cache.messages

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
        if cache.is_unrequested:
            self.refresh_messages(conversation_id)
        cache.appendleft_messages(message)
        return message

    def messages(self, conversation_id: int) -> List[ChatMessage]:
        assert conversation_id in self._caches
        cache = self._caches[conversation_id]
        if cache.is_unrequested:
            self.refresh_messages(conversation_id)
        assert cache.messages is not None
        return list(cache.messages)
