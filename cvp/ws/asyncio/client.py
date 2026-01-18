# -*- coding: utf-8 -*-

from asyncio import Task, sleep
from typing import Any, Optional, Union

import websockets

from cvp.logging.loggers import ws_logger as logger
from cvp.ws.handlers.message_handler import MessageHandler


class WebSocketClient:
    def __init__(
        self,
        uri: str,
        reconnect_interval: float = 5.0,
        handler: Optional[MessageHandler] = None,
    ):
        self._uri = uri
        self._reconnect_interval = reconnect_interval
        self._handler = handler
        self._ws: Optional[Any] = None
        self._running = False
        self._reconnect_task: Optional[Task] = None

    @property
    def uri(self) -> str:
        return self._uri

    async def connect(self) -> None:
        try:
            self._ws = await websockets.connect(self._uri)
            logger.info(f"WebSocket connected: {self._uri}")
        except Exception as e:
            logger.error(f"WebSocket connection failed: {e}")
            raise

    async def disconnect(self) -> None:
        if self._ws:
            await self._ws.close()
            self._ws = None
            logger.info("WebSocket disconnected")

    async def send(self, message: str) -> None:
        if not self._ws:
            raise RuntimeError("WebSocket is not connected")

        try:
            await self._ws.send(message)
            logger.debug(f"Message sent: {message}")
        except Exception as e:
            logger.error(f"Failed to send message: {e}")
            raise

    async def send_binary(self, data: bytes) -> None:
        if not self._ws:
            raise RuntimeError("WebSocket is not connected")

        try:
            await self._ws.send(data)
            logger.debug(f"Binary sent: {len(data)} bytes")
        except Exception as e:
            logger.error(f"Failed to send binary: {e}")
            raise

    async def receive(self) -> Union[str, bytes]:
        if not self._ws:
            raise RuntimeError("WebSocket is not connected")

        try:
            message = await self._ws.recv()
            if isinstance(message, bytes):
                logger.debug(f"Binary received: {len(message)} bytes")
            else:
                logger.debug(f"Message received: {message}")
            return message
        except Exception as e:
            logger.error(f"Failed to receive message: {e}")
            raise

    async def start(self) -> None:
        self._running = True

        while self._running:
            try:
                await self.connect()

                # Notify handler of connection
                if self._handler:
                    self._handler.on_connect()

                while self._running and self._ws:
                    try:
                        message = await self.receive()
                        # Dispatch based on message type
                        if isinstance(message, bytes):
                            await self.on_binary_message(message)
                        else:
                            await self.on_message(message)
                    except websockets.exceptions.ConnectionClosed:
                        logger.warning("WebSocket connection closed")
                        break
                    except Exception as e:
                        logger.error(f"Error during message processing: {e}")
                        break

            except Exception as e:
                logger.error(f"WebSocket connection error: {e}")

            finally:
                # Notify handler of disconnection
                if self._handler:
                    self._handler.on_disconnect()
                await self.disconnect()

            # Wait for reconnection
            if self._running:
                logger.info(f"Reconnecting in {self._reconnect_interval} seconds...")
                await sleep(self._reconnect_interval)

    async def stop(self) -> None:
        self._running = False
        await self.disconnect()
        logger.info("WebSocket client stopped")

    async def on_message(self, message: str) -> None:
        """Handle incoming text message. Override in subclass if needed."""
        logger.info(f"Received message: {message}")

    async def on_binary_message(self, data: bytes) -> None:
        """Handle incoming binary message.

        If a MessageHandler is set, delegates to it and sends response if any.
        Override in subclass for custom handling.
        """
        if self._handler:
            response = self._handler.on_message(data)
            if response:
                await self.send_binary(response)
        else:
            logger.info(f"Received binary: {len(data)} bytes")

    @property
    def is_connected(self) -> bool:
        if self._ws is None:
            return False
        return not getattr(self._ws, "closed", False)

    @property
    def handler(self) -> Optional[MessageHandler]:
        return self._handler

    @handler.setter
    def handler(self, value: Optional[MessageHandler]) -> None:
        self._handler = value
