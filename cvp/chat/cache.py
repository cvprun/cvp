# -*- coding: utf-8 -*-

from datetime import datetime
from io import StringIO
from typing import Iterable, List, Mapping, Optional

from ollama import Message

from cvp.chat.conversation import ChatConversation
from cvp.chat.ids import INVALID_CONVERSATION_ID, ChatConversationID, ChatMessageID
from cvp.chat.message import ChatMessage
from cvp.chat.stream import ChatStream


class ChatCache:
    def __init__(
        self,
        conversation: ChatConversation,
        messages: Optional[Iterable[ChatMessage]] = None,
        streams: Optional[Mapping[ChatMessageID, List[ChatStream]]] = None,
    ):
        self._conversation = conversation
        self._messages = list(messages if messages else ())
        self._streams = dict(streams if streams else {})

    @property
    def is_invalid_conversation_id(self) -> bool:
        return self.conversation_id == INVALID_CONVERSATION_ID

    @property
    def conversation_id(self) -> ChatConversationID:
        return self._conversation.id

    @property
    def conversation_title(self) -> str:
        return self._conversation.title

    @property
    def label(self) -> str:
        conv_title = self.conversation_title
        conv_id = self.conversation_id
        return (conv_title if conv_title else str(conv_id)) + f"###{conv_id}"

    @property
    def created_at(self) -> datetime:
        return self._conversation.created_at

    @property
    def updated_at(self) -> Optional[datetime]:
        return self._conversation.updated_at

    @property
    def messages(self) -> List[ChatMessage]:
        return self._messages

    def clear_messages(self) -> None:
        self._messages.clear()

    def set_messages(self, messages: Iterable[ChatMessage]) -> None:
        self._messages = list(messages if messages else ())

    def append_messages(self, *messages: ChatMessage) -> None:
        for message in messages:
            self._messages.append(message)

    def find_message(self, message_id: ChatMessageID) -> ChatMessage:
        for msg in self._messages:
            if msg.id == message_id:
                return msg
        raise IndexError(f"Not found message: {message_id}")

    @property
    def streams(self):
        return self._streams

    def add_stream(self, message_id: ChatMessageID, stream: ChatStream) -> None:
        if message_id in self._streams:
            self._streams[message_id].append(stream)
        else:
            self._streams[message_id] = [stream]

    def get_merged_response_message(self, message_id: ChatMessageID) -> Message:
        streams = self._streams[message_id]

        first_stream = streams[0]
        first_chunk = first_stream.load_chunk()
        first_message = first_chunk.message
        first_content = first_message.content if first_message.content else str()
        assert first_message.role == "assistant"
        assert first_message.images is None

        result_message = first_message.model_copy()
        result_message.content = first_content

        if len(streams) == 1:
            return result_message

        buffer = StringIO()
        buffer.write(first_content)

        for stream in streams[1:]:
            chunk = stream.load_chunk()
            assert first_message.role == chunk.message.role
            content = chunk.message.content if chunk.message.content else str()
            buffer.write(content)

        result_message.content = buffer.getvalue().strip()
        return result_message
