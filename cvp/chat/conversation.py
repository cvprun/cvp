# -*- coding: utf-8 -*-

from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional

from cvp.variables import INVALID_CHAT_ID


@dataclass
class ChatConversation:
    id: int = INVALID_CHAT_ID
    title: str = field(default_factory=str)
    created_at: datetime = field(default_factory=lambda: datetime.now().astimezone())
    updated_at: Optional[datetime] = None

    @classmethod
    def from_row(cls, row):
        assert isinstance(row, tuple)
        assert 4 == len(row)
        id_, title, created_at, updated_at = row
        assert isinstance(id_, int)
        assert isinstance(title, str)
        assert isinstance(created_at, str)
        assert isinstance(updated_at, (type(None), str))
        return cls(
            id_,
            title,
            datetime.fromisoformat(created_at).astimezone(),
            datetime.fromisoformat(updated_at).astimezone() if updated_at else None,
        )
