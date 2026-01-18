# -*- coding: utf-8 -*-

from cvp.logging.loggers import hub_logger as logger
from cvp.ws.handlers.agent_handler import AgentHandler
from cvp.ws.threading.server import WebSocketServer


class HubManager:
    def __init__(self, host: str = "localhost", port: int = 8765) -> None:
        self._host = host
        self._port = port
        self._handler = AgentHandler()
        self._server = WebSocketServer(host, port, handler=self._handler)

    def start(self) -> None:
        logger.info(f"Starting Hub server on ws://{self._host}:{self._port}")
        self._server.start()

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
        return self._host

    @property
    def port(self) -> int:
        return self._port
