# -*- coding: utf-8 -*-

from typing import NamedTuple, Optional, Sequence, Union

from ollama import Image, Message

from cvp.context.mixins._base import BaseContextMixin
from cvp.logging.logging import logger as logger
from cvp.variables import NOT_FOUND_INDEX


class ChatMixin(BaseContextMixin):
    @property
    def _ollama_chat_runner(self):
        return self.get_thread_runner(self.__on_ollama_chat_main)

    def __on_ollama_chat_main(
        self,
        conversation_id: int,
        server_key: str,
        model_name: str,
        content: str,
        images: Optional[Sequence[Union[str, bytes]]] = None,
    ) -> None:
        message = Message(
            role="user",
            content=content,
            images=tuple(Image(value=img) for img in images) if images else None,
            tool_calls=None,
        )
        request = message.model_dump_json()

        if conversation_id == NOT_FOUND_INDEX:
            cache = self._chat.create_new_chat_stream(title=str(), request=request)
            assert 1 == len(cache.messages)
            msg = cache.messages[0]
        else:
            cache = self._chat[conversation_id]
            msg = self._chat.append_chat(conversation_id, request)

        ollama = self._ollamas[server_key]
        model_index = ollama.model_names.index(model_name)
        assert 0 <= model_index < len(ollama.model_names)

        messages = tuple(msg.load_request() for msg in cache.messages)
        stream = ollama.client.chat(
            model=model_name,
            messages=messages,
            stream=True,
        )

        for response in stream:
            self._chat.append_stream(msg.id, response)

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
