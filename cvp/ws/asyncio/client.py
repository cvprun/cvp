# -*- coding: utf-8 -*-

from asyncio import Task, sleep
from typing import Any, Optional

import websockets

from cvp.logging.loggers import ws_logger as logger


class WebSocketClient:
    def __init__(self, uri: str, reconnect_interval: float = 5.0):
        self._uri = uri
        self._reconnect_interval = reconnect_interval
        self._ws: Optional[Any] = None
        self._running = False
        self._reconnect_task: Optional[Task] = None

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

    async def receive(self) -> str:
        if not self._ws:
            raise RuntimeError("WebSocket is not connected")

        try:
            message = await self._ws.recv()
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

                while self._running and self._ws:
                    try:
                        message = await self.receive()
                        # TODO:
                        # Implement message processing logic here or
                        # call method that subclasses can override
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
        logger.info(f"Received message: {message}")

    @property
    def is_connected(self) -> bool:
        if self._ws is None:
            return False
        return not getattr(self._ws, "closed", False)
