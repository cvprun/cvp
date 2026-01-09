# -*- coding: utf-8 -*-

import asyncio
from typing import Optional

from cvp.apps.agent.ws_client import WebSocketClient
from cvp.context.context import Context
from cvp.logging.loggers import logger


class AgentApplication:
    def __init__(self, context: Context):
        self._context = context
        self._ws_client: Optional[WebSocketClient] = None
        self._loop: Optional[asyncio.AbstractEventLoop] = None

    def start(self) -> None:
        """Agent 애플리케이션 시작"""
        # WebSocket URI 설정 (환경 변수나 설정 파일에서 가져올 수 있음)
        ws_uri = "ws://localhost:8765"  # 기본값

        # 설정에서 URI 가져오기 (있다면)
        if hasattr(self._context, "config"):
            ws_uri = getattr(self._context.config, "agent_ws_uri", ws_uri)

        logger.info(f"Agent 애플리케이션 시작: {ws_uri}")

        # WebSocket 클라이언트 생성
        self._ws_client = WebSocketClient(uri=ws_uri)

        # 이벤트 루프 생성 및 실행
        try:
            self._loop = asyncio.new_event_loop()
            asyncio.set_event_loop(self._loop)

            # WebSocket 클라이언트 시작
            self._loop.run_until_complete(self._run())
        except KeyboardInterrupt:
            logger.info("Agent 애플리케이션 중지 요청")
        finally:
            self._cleanup()

    async def _run(self) -> None:
        """비동기 실행 로직"""
        try:
            # WebSocket 클라이언트 시작
            await self._ws_client.start()
        except Exception as e:
            logger.error(f"Agent 실행 중 오류: {e}")
            raise

    def _cleanup(self) -> None:
        """정리 작업"""
        if self._ws_client:
            # WebSocket 클라이언트 중지
            if self._loop and not self._loop.is_closed():
                self._loop.run_until_complete(self._ws_client.stop())

        if self._loop:
            self._loop.close()

        logger.info("Agent 애플리케이션 종료")
