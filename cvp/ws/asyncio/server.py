# -*- coding: utf-8 -*-

import asyncio
from typing import Any, Awaitable, Callable, Optional, Set

import websockets

from cvp.logging.loggers import logger


class WebSocketServer:
    """순수 asyncio 기반 WebSocket 서버"""

    def __init__(
        self,
        host: str = "localhost",
        port: int = 8765,
        message_handler: Optional[Callable[[Any, str], Awaitable[None]]] = None,
    ):
        """
        Args:
            host: 서버 호스트 주소
            port: 서버 포트 번호
            message_handler: 메시지 처리 핸들러 함수
        """
        self._host = host
        self._port = port
        self._message_handler = message_handler or self._default_message_handler
        self._clients: Set[Any] = set()
        self._server: Any = None
        self._running = False

    async def _default_message_handler(self, websocket: Any, message: str) -> None:
        """
        기본 메시지 핸들러 - 에코 서버

        Args:
            websocket: 클라이언트 WebSocket 연결
            message: 수신된 메시지
        """
        logger.info(f"수신된 메시지: {message}")
        # 에코: 받은 메시지를 그대로 돌려보냄
        await websocket.send(f"Echo: {message}")

    async def _handle_client(self, websocket: Any) -> None:
        """
        클라이언트 연결 처리

        Args:
            websocket: 클라이언트 WebSocket 연결
        """
        # 클라이언트 등록
        self._clients.add(websocket)
        client_info = f"{websocket.remote_address[0]}:{websocket.remote_address[1]}"
        logger.info(f"클라이언트 연결: {client_info} (총 {len(self._clients)}명)")

        try:
            async for message in websocket:
                try:
                    # 메시지 핸들러 호출
                    await self._message_handler(websocket, message)
                except Exception as e:
                    logger.error(f"메시지 처리 중 오류 ({client_info}): {e}")
                    await websocket.send(f"Error: {str(e)}")

        except websockets.exceptions.ConnectionClosed:
            logger.info(f"클라이언트 연결 종료: {client_info}")
        except Exception as e:
            logger.error(f"클라이언트 처리 중 오류 ({client_info}): {e}")
        finally:
            # 클라이언트 제거
            self._clients.discard(websocket)
            logger.info(
                f"클라이언트 제거: {client_info} (남은 연결: {len(self._clients)}명)"
            )

    async def start(self) -> None:
        """WebSocket 서버 시작"""
        if self._running:
            logger.warning("서버가 이미 실행 중입니다")
            return

        self._running = True

        async with websockets.serve(
            self._handle_client, self._host, self._port
        ) as server:
            self._server = server
            logger.info(f"WebSocket 서버 시작: ws://{self._host}:{self._port}")

            # 서버가 중지될 때까지 대기
            await asyncio.Future()  # 무한 대기

    async def stop(self) -> None:
        """서버 중지"""
        if not self._running:
            logger.warning("서버가 실행 중이 아닙니다")
            return

        self._running = False

        # 모든 클라이언트 연결 종료
        if self._clients:
            logger.info(f"{len(self._clients)}개의 클라이언트 연결 종료 중...")
            await self._close_all_clients()

        logger.info("WebSocket 서버 중지")

    async def _close_all_clients(self) -> None:
        """모든 클라이언트 연결 종료"""
        if self._clients:
            await asyncio.gather(
                *[client.close() for client in self._clients],
                return_exceptions=True,
            )

    async def broadcast(self, message: str) -> None:
        """
        모든 연결된 클라이언트에게 메시지 브로드캐스트

        Args:
            message: 전송할 메시지
        """
        if not self._clients:
            logger.debug("연결된 클라이언트가 없습니다")
            return

        logger.debug(f"{len(self._clients)}명에게 브로드캐스트: {message}")

        # 연결이 끊긴 클라이언트 제거를 위한 리스트
        disconnected = set()

        for client in self._clients:
            try:
                await client.send(message)
            except websockets.exceptions.ConnectionClosed:
                disconnected.add(client)
            except Exception as e:
                logger.error(f"브로드캐스트 중 오류: {e}")
                disconnected.add(client)

        # 연결이 끊긴 클라이언트 제거
        self._clients -= disconnected

    @property
    def is_running(self) -> bool:
        """서버 실행 상태 확인"""
        return self._running

    @property
    def client_count(self) -> int:
        """연결된 클라이언트 수"""
        return len(self._clients)
