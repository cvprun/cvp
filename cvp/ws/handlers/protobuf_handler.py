# -*- coding: utf-8 -*-

from struct import pack, unpack
from typing import Callable, Dict, Final, Optional, Tuple, Type

from cvp.types.override import override
from cvp.ws.handlers.message_handler import MessageHandler

MSG_TYPE_MIN: Final[int] = 0
MSG_TYPE_MAX: Final[int] = 65535

HandlerCallable = Callable[[bytes], Optional[bytes]]


class ProtobufHandler(MessageHandler):
    """Handler for protobuf binary messages with type-based dispatch.

    Message format: [msg_type: uint16][payload: bytes]
    The first 2 bytes indicate the message type (big-endian),
    followed by the serialized protobuf payload.
    """

    handlers: Dict[int, HandlerCallable]
    message_types: Dict[int, Type]

    def __init__(self) -> None:
        self._handlers: Dict[int, Callable[[bytes], Optional[bytes]]] = {}
        self._message_types: Dict[int, Type] = {}

    def register(
        self,
        msg_type: int,
        handler: Callable[[bytes], Optional[bytes]],
        proto_class: Optional[Type] = None,
    ) -> None:
        """Register a handler for a specific message type."""
        if not MSG_TYPE_MIN <= msg_type <= MSG_TYPE_MAX:
            raise ValueError(
                f"msg_type must be {MSG_TYPE_MIN}-{MSG_TYPE_MAX}, got {msg_type}"
            )
        self._handlers[msg_type] = handler
        if proto_class is not None:
            self._message_types[msg_type] = proto_class

    def unregister(self, msg_type: int) -> None:
        """Unregister a handler for a message type."""
        self._handlers.pop(msg_type, None)
        self._message_types.pop(msg_type, None)

    def dispatch(self, data: bytes) -> Optional[bytes]:
        """Parse message type and dispatch to registered handler."""
        msg_type, payload = self._parse_message(data)
        if msg_type is None:
            return None

        handler = self._handlers.get(msg_type)
        if handler is None:
            return None

        return handler(payload)

    @staticmethod
    def _parse_message(data: bytes) -> Tuple[Optional[int], bytes]:
        """Parse message type and payload from raw data."""
        if len(data) < 2:
            return None, b""

        msg_type = unpack(">H", data[:2])[0]
        payload = data[2:]
        return msg_type, payload

    @staticmethod
    def encode_message(msg_type: int, payload: bytes) -> bytes:
        """Encode a message with type prefix."""
        return pack(">H", msg_type) + payload

    @override
    def on_message(self, data: bytes) -> Optional[bytes]:
        """Handle incoming message by dispatching to registered handler."""
        return self.dispatch(data)

    @override
    def on_connect(self) -> None:
        """Called when a client connects."""
        pass

    @override
    def on_disconnect(self) -> None:
        """Called when a client disconnects."""
        pass

    def get_message_type(self, msg_type: int) -> Optional[Type]:
        """Get registered protobuf class for a message type."""
        return self._message_types.get(msg_type)
