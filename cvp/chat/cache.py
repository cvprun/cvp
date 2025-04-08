# -*- coding: utf-8 -*-

from collections import deque
from datetime import datetime
from typing import Iterable, Optional

from cvp.chat.conversation import ChatConversation
from cvp.chat.message import ChatMessage


class Cache:
    def __init__(
        self,
        conversation: ChatConversation,
        messages: Optional[Iterable[ChatMessage]] = None,
    ):
        self._conversation = conversation
        self._messages = deque(messages) if messages else None

    @property
    def id(self) -> int:
        return self._conversation.id

    @property
    def title(self) -> str:
        return self._conversation.title

    @property
    def label(self) -> str:
        return (self.title if self.title else str(self.id)) + f"###{self.id}"

    @property
    def created_at(self) -> datetime:
        return self._conversation.created_at

    @property
    def updated_at(self) -> Optional[datetime]:
        return self._conversation.updated_at

    @property
    def messages(self):
        return self._messages

    def appendleft_messages(self, messages: Iterable[ChatMessage]) -> None:
        if self._messages is None:
            self._messages = deque()
        for msg in messages:
            self._messages.appendleft(msg)
