# -*- coding: utf-8 -*-

from dataclasses import dataclass, field
from datetime import datetime
from typing import Any, Optional

import orjson

from cvp.variables import INVALID_CHAT_ID


@dataclass
class ChatStream:
    id: int = INVALID_CHAT_ID
    message_id: int = INVALID_CHAT_ID
    chunk: Optional[str] = None
    created_at: datetime = field(default_factory=lambda: datetime.now().astimezone())

    def dump_chunk(self, data: Any) -> None:
        self.chunk = str(orjson.dumps(data), encoding="utf-8")

    def load_chunk(self) -> Any:
        return orjson.loads(self.chunk) if self.chunk else None

    @classmethod
    def from_row(cls, row):
        assert isinstance(row, tuple)
        assert 4 == len(row)
        id_, message_id, chunk, created_at = row
        assert isinstance(id_, int)
        assert isinstance(message_id, int)
        assert isinstance(chunk, (type(None), str))
        assert isinstance(created_at, str)
        return cls(
            id_,
            message_id,
            chunk,
            datetime.fromisoformat(created_at).astimezone(),
        )
