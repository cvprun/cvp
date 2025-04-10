# -*- coding: utf-8 -*-

from dataclasses import dataclass, field
from datetime import datetime

from ollama import ChatResponse

from cvp.variables import INVALID_CHAT_ID


@dataclass
class ChatStream:
    id: int = INVALID_CHAT_ID
    message_id: int = INVALID_CHAT_ID
    chunk: str = field(default_factory=str)
    created_at: datetime = field(default_factory=lambda: datetime.now().astimezone())

    def dump_chunk(self, data: ChatResponse) -> None:
        self.chunk = data.model_dump_json()

    def load_chunk(self) -> ChatResponse:
        return ChatResponse.model_validate_json(self.chunk)

    @classmethod
    def from_row(cls, row):
        assert isinstance(row, tuple)
        assert 4 == len(row)
        id_, message_id, chunk, created_at = row
        assert isinstance(id_, int)
        assert isinstance(message_id, int)
        assert isinstance(chunk, str)
        assert isinstance(created_at, str)
        return cls(
            id_,
            message_id,
            chunk,
            datetime.fromisoformat(created_at).astimezone(),
        )
