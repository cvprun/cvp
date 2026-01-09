# -*- coding: utf-8 -*-

import asyncio
from typing import Optional

import websockets
from websockets.client import WebSocketClientProtocol

from cvp.logging.loggers import logger


class WebSocketClient:
    """비동기 WebSocket 클라이언트"""

    def __init__(self, uri: str, reconnect_interval: float = 5.0):
        """
        Args:
            uri: WebSocket 서버 URI (예: ws://localhost:8765)
            reconnect_interval: 재연결 시도 간격(초)
        """
        self._uri = uri
        self._reconnect_interval = reconnect_interval
        self._ws: Optional[WebSocketClientProtocol] = None
        self._running = False
        self._reconnect_task: Optional[asyncio.Task] = None

    async def connect(self) -> None:
        """WebSocket 서버에 연결"""
        try:
            self._ws = await websockets.connect(self._uri)
            logger.info(f"WebSocket 연결 성공: {self._uri}")
        except Exception as e:
            logger.error(f"WebSocket 연결 실패: {e}")
            raise

    async def disconnect(self) -> None:
        """WebSocket 연결 종료"""
        if self._ws:
            await self._ws.close()
            self._ws = None
            logger.info("WebSocket 연결 종료")

    async def send(self, message: str) -> None:
        """메시지 전송"""
        if not self._ws:
            raise RuntimeError("WebSocket이 연결되지 않았습니다")

        try:
            await self._ws.send(message)
            logger.debug(f"메시지 전송: {message}")
        except Exception as e:
            logger.error(f"메시지 전송 실패: {e}")
            raise

    async def receive(self) -> str:
        """메시지 수신"""
        if not self._ws:
            raise RuntimeError("WebSocket이 연결되지 않았습니다")

        try:
            message = await self._ws.recv()
            logger.debug(f"메시지 수신: {message}")
            return message
        except Exception as e:
            logger.error(f"메시지 수신 실패: {e}")
            raise

    async def start(self) -> None:
        """WebSocket 클라이언트 시작 (자동 재연결 포함)"""
        self._running = True

        while self._running:
            try:
                await self.connect()

                # 연결이 유지되는 동안 메시지 수신 처리
                while self._running and self._ws:
                    try:
                        message = await self.receive()
                        # 메시지 처리 로직을 여기에 구현하거나
                        # 서브클래스에서 오버라이드할 수 있도록 메서드 호출
                        await self.on_message(message)
                    except websockets.exceptions.ConnectionClosed:
                        logger.warning("WebSocket 연결이 닫혔습니다")
                        break
                    except Exception as e:
                        logger.error(f"메시지 처리 중 오류: {e}")
                        break

            except Exception as e:
                logger.error(f"WebSocket 연결 오류: {e}")

            finally:
                await self.disconnect()

            # 재연결 대기
            if self._running:
                logger.info(f"{self._reconnect_interval}초 후 재연결 시도...")
                await asyncio.sleep(self._reconnect_interval)

    async def stop(self) -> None:
        """WebSocket 클라이언트 중지"""
        self._running = False
        await self.disconnect()
        logger.info("WebSocket 클라이언트 중지")

    async def on_message(self, message: str) -> None:
        """
        메시지 수신 시 호출되는 핸들러
        서브클래스에서 오버라이드하여 사용

        Args:
            message: 수신된 메시지
        """
        logger.info(f"수신된 메시지: {message}")

    @property
    def is_connected(self) -> bool:
        """연결 상태 확인"""
        return self._ws is not None and not self._ws.closed
