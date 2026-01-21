# -*- coding: utf-8 -*-

from cvp.hub.agent_handler import AgentHandler
from cvp.logging.loggers import hub_logger as logger
from cvp.variables import EPHEMERAL_PORT, LOCALHOST
from cvp.ws.threading.server import WebSocketServer


class HubManager:
    def __init__(self, host: str = LOCALHOST, port: int = EPHEMERAL_PORT) -> None:
        self._handler = AgentHandler()
        self._server = WebSocketServer(host, port, handler=self._handler)

    def start(self) -> None:
        self._server.start()
        logger.info(f"Hub server started on ws://{self.host}:{self.port}")

    def stop(self) -> None:
        logger.info("Stopping Hub server")
        self._server.stop()

    @property
    def session_count(self) -> int:
        return self._handler.session_count

    @property
    def is_running(self) -> bool:
        return self._server.is_running

    @property
    def host(self) -> str:
        return self._server.host

    @property
    def port(self) -> int:
        """Return the actual bound port. Returns -1 if not yet bound."""
        return self._server.port
