# -*- coding: utf-8 -*-

from typing import NamedTuple

from cvp.context.mixins._base import BaseContextMixin
from cvp.logging.logging import logger as logger


class ChatMixin(BaseContextMixin):
    @property
    def _ollama_chat_runner(self):
        return self.get_thread_runner(self.__on_ollama_chat_main)

    def __on_ollama_chat_main(
        self,
        conversation_id: int,
        server_key: str,
        model_name: str,
        message: str,
    ) -> None:
        cache = self._chat[conversation_id]
        assert cache.id == conversation_id
        assert not cache.has_live

        ollama = self._ollamas[server_key]
        model_index = ollama.model_names.index(model_name)
        assert 0 <= model_index < len(ollama.model_names)

        # messages = list(cache.messages)
        # msg = cache.create_invalid_chat_message()
        # msg.dump_first_user_message_request(message)

        stream = ollama.client.chat(
            model=model_name,
            messages=[{"role": "user", "content": message}],
            stream=True,
        )

        for chunk in stream:
            print(chunk["message"]["content"], end="", flush=True)

    @property
    def chat_model_names(self):
        return self._config.chat.model_names

    def refresh_chat_models(self) -> None:
        self._config.chat.clear_models()

        for key, ollama in self._ollamas.items():
            for model_name in ollama.model_names:
                self._config.chat.append_models(key, ollama.name, model_name)

    class _OllamaChatStatus(NamedTuple):
        has_error: bool
        error_message: str
        running: bool

    def get_ollama_chat_status(self):
        has_error = bool(self._ollama_chat_runner.error)
        error_message = str(self._ollama_chat_runner.error)
        running = self._ollama_chat_runner.running

        return self._OllamaChatStatus(
            has_error=has_error,
            error_message=error_message,
            running=running,
        )

    def request_chat_stream(
        self,
        conversation_id: int,
        server_key: str,
        model_name: str,
        message: str,
    ) -> None:
        if self._ollama_chat_runner.running:
            raise ValueError("The ollama chat runner is running")

        logger.info(f"Request chat stream: '{message}'")
        self._ollama_chat_runner(conversation_id, server_key, model_name, message)
