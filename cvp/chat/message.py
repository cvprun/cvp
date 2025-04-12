# -*- coding: utf-8 -*-

from dataclasses import dataclass, field
from datetime import datetime
from http import HTTPStatus
from typing import Optional

from ollama import Message

from cvp.chat.ids import (
    INVALID_CONVERSATION_ID,
    INVALID_MESSAGE_ID,
    ChatConversationID,
    ChatMessageID,
)


@dataclass
class ChatMessage:
    id: ChatMessageID = INVALID_MESSAGE_ID
    conversation_id: ChatConversationID = INVALID_CONVERSATION_ID
    request: str = field(default_factory=str)
    error: str = field(default_factory=str)
    status: int = 0
    created_at: datetime = field(default_factory=lambda: datetime.now().astimezone())
    updated_at: Optional[datetime] = None

    @property
    def http_status(self) -> HTTPStatus:
        return HTTPStatus(self.status)

    @property
    def is_ok(self) -> bool:
        return self.status == int(HTTPStatus.OK)

    @property
    def is_invalid_id(self) -> bool:
        return self.id == INVALID_MESSAGE_ID

    @property
    def is_invalid_conversation_id(self) -> bool:
        return self.conversation_id == INVALID_CONVERSATION_ID

    def dump_request(self, data: Message) -> None:
        self.request = data.model_dump_json()

    def load_request(self) -> Message:
        return Message.model_validate_json(self.request)

    @classmethod
    def from_row(cls, row):
        assert isinstance(row, tuple)
        assert 7 == len(row)
        id_, conversation_id, request, error, status, created_at, updated_at = row
        assert isinstance(id_, int)
        assert isinstance(conversation_id, int)
        assert isinstance(request, str)
        assert isinstance(error, str)
        assert isinstance(status, int)
        assert isinstance(created_at, str)
        assert isinstance(updated_at, (type(None), str))
        return cls(
            ChatMessageID(id_),
            ChatConversationID(conversation_id),
            request,
            error,
            status,
            datetime.fromisoformat(created_at).astimezone(),
            datetime.fromisoformat(updated_at).astimezone() if updated_at else None,
        )
