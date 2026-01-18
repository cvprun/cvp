# -*- coding: utf-8 -*-

from abc import ABC, abstractmethod
from typing import Optional


class MessageHandler(ABC):
    """Abstract base class for WebSocket message handlers."""

    @abstractmethod
    def on_message(self, data: bytes) -> Optional[bytes]:
        """Handle incoming message and optionally return response."""
        raise NotImplementedError

    @abstractmethod
    def on_connect(self) -> None:
        """Called when a client connects."""
        raise NotImplementedError

    @abstractmethod
    def on_disconnect(self) -> None:
        """Called when a client disconnects."""
        raise NotImplementedError
