from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass
class ChatMessage:
    id: int
    conversation_id: int
    request: Optional[str]
    response: Optional[str]
    error: Optional[str]
    created_at: datetime

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
