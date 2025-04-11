# -*- coding: utf-8 -*-

from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional

from ollama import Message

from cvp.variables import CHAT_INVALID_ID


@dataclass
class ChatMessage:
    id: int = CHAT_INVALID_ID
    conversation_id: int = CHAT_INVALID_ID
    request: str = field(default_factory=str)
    error: Optional[str] = None
    status: int = 0
    created_at: datetime = field(default_factory=lambda: datetime.now().astimezone())
    updated_at: Optional[datetime] = None

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
        assert isinstance(error, (type(None), str))
        assert isinstance(status, int)
        assert isinstance(created_at, str)
        assert isinstance(updated_at, (type(None), str))
        return cls(
            id_,
            conversation_id,
            request,
            error,
            status,
            datetime.fromisoformat(created_at).astimezone(),
            datetime.fromisoformat(updated_at).astimezone() if updated_at else None,
        )
