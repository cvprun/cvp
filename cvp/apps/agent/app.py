# -*- coding: utf-8 -*-

from asyncio import get_running_loop

from cvp.aio.run import aio_run
from cvp.logging.loggers import agent_logger as logger
from cvp.variables import AGENT_WS_ADDRESS, LOGGING_STEP, SLOW_CALLBACK_DURATION
from cvp.ws.asyncio.client import WebSocketClient
from cvp.ws.handlers.protobuf_handler import ProtobufHandler


class AgentApplication(ProtobufHandler):
    def __init__(
        self,
        ws_uri: str = AGENT_WS_ADDRESS,
        logging_step=LOGGING_STEP,
        slow_callback_duration=SLOW_CALLBACK_DURATION,
        use_uvloop=False,
        debug=False,
        verbose=0,
    ):
        self._ws_client = WebSocketClient(uri=ws_uri)
        self._logging_step = logging_step
        self._slow_callback_duration = slow_callback_duration
        self._use_uvloop = use_uvloop
        self._debug = debug
        self._verbose = verbose

    async def on_main(self) -> None:
        logger.info(f"Starting agent application: {self._ws_client.uri}")

        loop = get_running_loop()
        loop.slow_callback_duration = self._slow_callback_duration
        loop.set_debug(self._debug)

        try:
            await self._ws_client.start()
        except Exception as e:
            logger.error(f"Agent runtime error: {e}")
            raise
        finally:
            await self._ws_client.stop()
            logger.info("Agent application stopped")

    def start(self) -> None:
        try:
            aio_run(self.on_main(), self._use_uvloop)
        except (KeyboardInterrupt, InterruptedError):
            logger.warning("Interrupt signal detected")
