# -*- coding: utf-8 -*-

from typing import Final, NewType

from cvp.variables import CHAT_INVALID_ID

ChatConversationID = NewType("ChatConversationID", int)
ChatMessageID = NewType("ChatMessageID", int)
ChatStreamID = NewType("ChatStreamID", int)

INVALID_CONVERSATION_ID: Final[ChatConversationID] = ChatConversationID(CHAT_INVALID_ID)
INVALID_MESSAGE_ID: Final[ChatMessageID] = ChatMessageID(CHAT_INVALID_ID)
INVALID_STREAM_ID: Final[ChatStreamID] = ChatStreamID(CHAT_INVALID_ID)
