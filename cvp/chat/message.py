# -*- coding: utf-8 -*-

from dataclasses import dataclass, field
from datetime import datetime
from typing import Any, Optional

import orjson

from cvp.variables import INVALID_CHAT_ID


@dataclass
class ChatMessage:
    id: int = INVALID_CHAT_ID
    conversation_id: int = INVALID_CHAT_ID
    request: Optional[str] = None
    error: Optional[str] = None
    status: int = 0
    created_at: datetime = field(default_factory=lambda: datetime.now().astimezone())
    updated_at: Optional[datetime] = None

    def dump_first_user_message_request(self, message: str) -> None:
        self.dump_request({"role": "user", "content": message})

    def dump_request(self, data: Any) -> None:
        self.request = str(orjson.dumps(data), encoding="utf-8")

    def load_request(self) -> Any:
        return orjson.loads(self.request) if self.request else None

    @classmethod
    def from_row(cls, row):
        assert isinstance(row, tuple)
        assert 7 == len(row)
        id_, conversation_id, request, error, status, created_at, updated_at = row
        assert isinstance(id_, int)
        assert isinstance(conversation_id, int)
        assert isinstance(request, (type(None), str))
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
