# -*- coding: utf-8 -*-

from http import HTTPStatus
from typing import Dict, Optional, TypeAlias, Union

from ollama import ChatResponse

from cvp.chat.cache import ChatCache
from cvp.chat.conversation import ChatConversation
from cvp.chat.database import ChatDatabase
from cvp.chat.ids import ChatConversationID, ChatMessageID
from cvp.chat.message import ChatMessage
from cvp.chat.stream import ChatStream
from cvp.chrono.isoformat import DateTimeLike, fromisoformat, isoformat_with_utc
from cvp.resources.subdirs.chat import ChatPath
from cvp.variables import CHAT_LIMIT, NOT_FOUND_INDEX

ChatCacheDict: TypeAlias = Dict[ChatConversationID, ChatCache]


class ChatManager:
    _caches: ChatCacheDict

    def __init__(
        self,
        path: ChatPath,
        limit=CHAT_LIMIT,
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
            self.reload_database()

    def reload_database(self) -> None:
        self._caches = self.read_caches()

    def read_caches(self, limit: Optional[int] = None):
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

    def __getitem__(self, conv_id: ChatConversationID):
        return self._caches[conv_id]

    def __setitem__(self, conv_id: ChatConversationID, value: ChatCache):
        self._caches[conv_id] = value

    def __delitem__(self, conv_id: ChatConversationID):
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
        assert isinstance(ids, tuple)
        assert 2 == len(ids)
        conv_id, msg_id = ids

        conv_row = conv_id, title, created_at, None
        conv = ChatConversation.from_row(conv_row)

        msg_row = msg_id, conv_id, request, str(), 0, created_at, None
        msg = ChatMessage.from_row(msg_row)

        assert conv_id not in self._caches
        cache = ChatCache(conv, (msg,))
        self._caches[conv_id] = cache

        assert cache.conversation_id != NOT_FOUND_INDEX
        assert 1 == len(cache.messages)
        assert cache.messages[0].id != NOT_FOUND_INDEX
        assert cache.messages[0].conversation_id == cache.conversation_id

        return cache

    def refresh_messages(self, conversation_id: ChatConversationID):
        if conversation_id not in self._caches:
            raise KeyError(f"Not found conversation: {conversation_id}")

        cache = self._caches[conversation_id]
        messages = self._database.select_message(conversation_id)
        cache.set_messages(messages)
        return cache.messages

    def append_chat(
        self,
        conversation_id: ChatConversationID,
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

    def messages(self, conversation_id: ChatConversationID):
        return self._caches[conversation_id].messages

    def find_cache_with_message_id(self, message_id: ChatMessageID) -> ChatCache:
        for cache in self._caches.values():
            try:
                msg = cache.find_message(message_id)
                assert msg.id == message_id
                return cache
            except IndexError:
                continue
        raise IndexError(f"Not found message: {message_id}")

    def update_message_result(
        self,
        message_id: ChatMessageID,
        error: str,
        status=0,
        updated_at: DateTimeLike = None,
        conversation_id: Optional[ChatConversationID] = None,
    ) -> ChatMessage:
        updated_at = isoformat_with_utc(updated_at)
        assert isinstance(updated_at, str)

        self._database.update_message_error_and_status(
            message_id,
            error,
            status,
            updated_at,
        )

        if conversation_id is not None:
            cache = self._caches[conversation_id]
        else:
            cache = self.find_cache_with_message_id(message_id)

        message = cache.find_message(message_id)
        message.error = error
        message.status = status
        message.updated_at = fromisoformat(updated_at)
        return message

    def update_message_ok(
        self,
        message_id: ChatMessageID,
        updated_at: DateTimeLike = None,
        conversation_id: Optional[ChatConversationID] = None,
    ):
        return self.update_message_result(
            message_id=message_id,
            error=str(),
            status=int(HTTPStatus.OK),
            updated_at=updated_at,
            conversation_id=conversation_id,
        )

    def update_message_error(
        self,
        message_id: ChatMessageID,
        error: str,
        status: Union[int, HTTPStatus],
        updated_at: DateTimeLike = None,
        conversation_id: Optional[ChatConversationID] = None,
    ):
        return self.update_message_result(
            message_id=message_id,
            error=error,
            status=int(status),
            updated_at=updated_at,
            conversation_id=conversation_id,
        )

    def append_stream(
        self,
        message_id: ChatMessageID,
        response: ChatResponse,
        created_at: DateTimeLike = None,
        conversation_id: Optional[ChatConversationID] = None,
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
