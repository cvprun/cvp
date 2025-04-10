# -*- coding: utf-8 -*-

from typing import Dict, Optional

from ollama import ChatResponse

from cvp.chat.cache import ChatCache
from cvp.chat.conversation import ChatConversation
from cvp.chat.database import ChatDatabase
from cvp.chat.message import ChatMessage
from cvp.chat.stream import ChatStream
from cvp.chrono.isoformat import DateTimeLike, isoformat_with_utc
from cvp.resources.subdirs.chat import ChatPath
from cvp.variables import DEFAULT_CHAT_LIMIT, NOT_FOUND_INDEX


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
        self._caches = self.read_conversations()

    def read_conversations(self, limit: Optional[int] = None):
        if limit is None:
            limit = self._limit
        assert isinstance(limit, int)

        caches = dict()
        for conv in self._database.select_conversation_latest(limit):
            messages = self._database.select_message(conv.id)
            streams = {m.id: self._database.select_stream(m.id) for m in messages}
            caches[conv.id] = ChatCache(conv, messages, streams)
        return caches

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

    def create_new_chat_stream(
        self,
        title: str,
        request: str,
        created_at: DateTimeLike = None,
    ) -> ChatCache:
        created_at = isoformat_with_utc(created_at)
        assert isinstance(created_at, str)

        ids = self._database.insert_conversation_and_message(title, request, created_at)
        conv_id, msg_id = ids

        conv_row = conv_id, title, created_at, None
        conv = ChatConversation.from_row(conv_row)

        msg_row = msg_id, conv_id, request, None, 0, created_at, None
        msg = ChatMessage.from_row(msg_row)

        assert conv_id not in self._caches
        cache = ChatCache(conv, (msg,))
        self._caches[conv_id] = cache

        assert cache.conversation_id != NOT_FOUND_INDEX
        assert 1 == len(cache.messages)
        assert cache.messages[0].id != NOT_FOUND_INDEX
        assert cache.messages[0].conversation_id == cache.conversation_id

        return cache

    def refresh_messages(self, conversation_id: int):
        if conversation_id not in self._caches:
            raise KeyError(f"Not found conversation: {conversation_id}")

        cache = self._caches[conversation_id]
        messages = self._database.select_message(conversation_id)
        cache.set_messages(messages)
        return cache.messages

    def append_chat(
        self,
        conversation_id: int,
        request: str,
        error: Optional[str] = None,
        status=0,
        created_at: DateTimeLike = None,
    ) -> ChatMessage:
        created_at = isoformat_with_utc(created_at)
        assert isinstance(created_at, str)

        if error is None:
            error = str()
        assert isinstance(error, str)

        msg_id = self._database.insert_message(
            conversation_id,
            request,
            error,
            status,
            created_at,
        )
        msg_row = msg_id, conversation_id, request, error, status, created_at, None
        message = ChatMessage.from_row(msg_row)

        self._caches[conversation_id].append_messages(message)
        return message

    def messages(self, conversation_id: int):
        return self._caches[conversation_id].messages

    def find_cache_with_message_id(self, message_id: int) -> ChatCache:
        for cache in self._caches.values():
            try:
                msg = cache.find_message(message_id)
                assert msg.id == message_id
                return cache
            except IndexError:
                continue
        raise IndexError(f"Not found message: {message_id}")

    def append_stream(
        self,
        message_id: int,
        response: ChatResponse,
        created_at: DateTimeLike = None,
        conversation_id: Optional[int] = None,
    ) -> ChatStream:
        created_at = isoformat_with_utc(created_at)
        assert isinstance(created_at, str)

        chunk = response.model_dump_json()
        stream_id = self._database.insert_stream(message_id, chunk, created_at)
        stream_row = stream_id, message_id, chunk, created_at
        stream = ChatStream.from_row(stream_row)

        if conversation_id is not None:
            cache = self._caches[conversation_id]
        else:
            cache = self.find_cache_with_message_id(message_id)
        cache.add_stream(message_id, stream)
        return stream
