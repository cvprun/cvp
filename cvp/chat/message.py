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
    response: Optional[str] = None
    error: Optional[str] = None
    created_at: datetime = field(default_factory=lambda: datetime.now().astimezone())

    def dump_first_user_message_request(self, message: str) -> None:
        self.dump_request({"role": "user", "content": message})

    def dump_request(self, data: Any) -> None:
        self.request = str(orjson.dumps(data), encoding="utf-8")

    def load_request(self) -> Any:
        return orjson.loads(self.request) if self.request else None

    def dump_response(self, data: Any) -> None:
        self.response = str(orjson.dumps(data), encoding="utf-8")

    def load_response(self) -> Any:
        return orjson.loads(self.response) if self.response else None

    @classmethod
    def from_row(cls, row):
        assert isinstance(row, tuple)
        assert 6 == len(row)
        id_, conversation_id, request, response, error, created_at = row
        assert isinstance(id_, int)
        assert isinstance(conversation_id, int)
        assert isinstance(request, (type(None), str))
        assert isinstance(response, (type(None), str))
        assert isinstance(error, (type(None), str))
        assert isinstance(created_at, str)
        return cls(
            id_,
            conversation_id,
            request,
            response,
            error,
            datetime.fromisoformat(created_at).astimezone(),
        )
