# -*- coding: utf-8 -*-

from dataclasses import dataclass, field
from datetime import datetime
from threading import Lock
from typing import Dict, Final, Optional

from cvp.logging.loggers import hub_logger as logger
from cvp.protos.agent_pb2 import Pat, Pit
from cvp.types.override import override
from cvp.ws.handlers.protobuf_handler import ProtobufHandler

MSG_TYPE_PIT: Final[int] = 1
MSG_TYPE_PAT: Final[int] = 2


@dataclass
class AgentSession:
    session_id: str
    connected_at: datetime = field(default_factory=datetime.now)
    last_heartbeat: Optional[datetime] = None


class AgentHandler(ProtobufHandler):
    def __init__(self) -> None:
        super().__init__()
        self._sessions: Dict[str, AgentSession] = {}
        self._sessions_lock = Lock()
        self._session_counter = 0

        self.register(MSG_TYPE_PIT, self._handle_pit, Pit)

    def _handle_pit(self, payload: bytes) -> Optional[bytes]:
        pit = Pit()
        pit.ParseFromString(payload)
        logger.debug(f"Received Pit: delay={pit.delay}")

        pat = Pat(ok=True)
        return self.encode_message(MSG_TYPE_PAT, pat.SerializeToString())

    @override
    def on_connect(self) -> None:
        with self._sessions_lock:
            self._session_counter += 1
            session_id = f"agent-{self._session_counter}"
            session = AgentSession(session_id=session_id)
            self._sessions[session_id] = session
            logger.info(f"Agent connected: {session_id}")

    @override
    def on_disconnect(self) -> None:
        with self._sessions_lock:
            if self._sessions:
                session_id = list(self._sessions.keys())[-1]
                del self._sessions[session_id]
                logger.info(f"Agent disconnected: {session_id}")

    @property
    def session_count(self) -> int:
        with self._sessions_lock:
            return len(self._sessions)
