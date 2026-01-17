# -*- coding: utf-8 -*-

import asyncio
from typing import Any, Awaitable, Callable, Optional, Set

import websockets

from cvp.logging.loggers import ws_logger as logger


class WebSocketServer:
    def __init__(
        self,
        host: str = "localhost",
        port: int = 8765,
        message_handler: Optional[Callable[[Any, str], Awaitable[None]]] = None,
    ):
        self._host = host
        self._port = port
        self._message_handler = message_handler or self._default_message_handler
        self._clients: Set[Any] = set()
        self._server: Any = None
        self._running = False

    async def _default_message_handler(self, websocket: Any, message: str) -> None:
        """
        Default message handler - echo server

        Args:
            websocket: Client WebSocket connection
            message: Received message
        """
        logger.info(f"Received message: {message}")
        # Echo: send back the received message
        await websocket.send(f"Echo: {message}")

    async def _handle_client(self, websocket: Any) -> None:
        """
        Handle client connection

        Args:
            websocket: Client WebSocket connection
        """
        # Register client
        self._clients.add(websocket)
        client_info = f"{websocket.remote_address[0]}:{websocket.remote_address[1]}"
        logger.info(f"Client connected: {client_info} (total {len(self._clients)})")

        try:
            async for message in websocket:
                try:
                    # Call message handler
                    await self._message_handler(websocket, message)
                except Exception as e:
                    logger.error(f"Error processing message ({client_info}): {e}")
                    await websocket.send(f"Error: {str(e)}")

        except websockets.exceptions.ConnectionClosed:
            logger.info(f"Client disconnected: {client_info}")
        except Exception as e:
            logger.error(f"Error handling client ({client_info}): {e}")
        finally:
            # Remove client
            self._clients.discard(websocket)
            logger.info(
                f"Client removed: {client_info} (remaining {len(self._clients)})"
            )

    async def start(self) -> None:
        """Start WebSocket server"""
        if self._running:
            logger.warning("Server is already running")
            return

        self._running = True

        async with websockets.serve(
            self._handle_client, self._host, self._port
        ) as server:
            self._server = server
            logger.info(f"WebSocket server started: ws://{self._host}:{self._port}")

            # Wait until server stops
            await asyncio.Future()  # Infinite wait

    async def stop(self) -> None:
        """Stop server"""
        if not self._running:
            logger.warning("Server is not running")
            return

        self._running = False

        # Close all client connections
        if self._clients:
            logger.info(f"Closing {len(self._clients)} client connection(s)...")
            await self._close_all_clients()

        logger.info("WebSocket server stopped")

    async def _close_all_clients(self) -> None:
        """Close all client connections"""
        if self._clients:
            await asyncio.gather(
                *[client.close() for client in self._clients],
                return_exceptions=True,
            )

    async def broadcast(self, message: str) -> None:
        """
        Broadcast message to all connected clients

        Args:
            message: Message to send
        """
        if not self._clients:
            logger.debug("No connected clients")
            return

        logger.debug(f"Broadcasting to {len(self._clients)} client(s): {message}")

        # List for removing disconnected clients
        disconnected = set()

        for client in self._clients:
            try:
                await client.send(message)
            except websockets.exceptions.ConnectionClosed:
                disconnected.add(client)
            except Exception as e:
                logger.error(f"Error during broadcast: {e}")
                disconnected.add(client)

        # Remove disconnected clients
        self._clients -= disconnected

    @property
    def is_running(self) -> bool:
        """Check server running status"""
        return self._running

    @property
    def client_count(self) -> int:
        """Number of connected clients"""
        return len(self._clients)
