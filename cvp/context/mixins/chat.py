# -*- coding: utf-8 -*-

from typing import List, NamedTuple, Optional, Sequence, Union

from ollama import Image, Message, ResponseError

from cvp.chat.ids import ChatConversationID, ChatMessageID
from cvp.context.mixins._base import BaseContextMixin
from cvp.logging.logging import chat_logger as logger
from cvp.ollama.manager import OllamaFilename
from cvp.ollama.ollama import Ollama
from cvp.variables import NOT_FOUND_INDEX, UNKNOWN_ERROR_CODE


class ChatMixin(BaseContextMixin):
    @property
    def _ollama_chat_runner(self):
        return self.get_thread_runner(self.__on_ollama_chat_main)

    def __on_ollama_chat_main(
        self,
        conversation_id: ChatConversationID,
        message_id: ChatMessageID,
        ollama: Ollama,
        model_name: str,
        messages: Sequence[Message],
        stream=False,
    ) -> None:
        assert conversation_id != NOT_FOUND_INDEX
        try:
            logger.info(
                f"Sending request to ollama at '{ollama.url}' "
                f"using model '{model_name}' ..."
            )

            response = ollama.client.chat(
                model=model_name,
                messages=messages,
                stream=stream,
            )

            if stream:
                logger.debug("Response streaming ...")
                for res in response:
                    logger.debug(f"Append stream chunk: {response}")
                    self._chat.append_stream(message_id, res)
                logger.debug("Response streaming is done")
            else:
                logger.debug(f"Append response: {response}")
                self._chat.append_stream(message_id, response)
        except ResponseError as e:
            logger.error(f"Ollama response {e.status_code} error: '{e}'")
            self._chat.update_message_error(
                message_id=message_id,
                error=e.error,
                status=e.status_code,
                updated_at=None,
                conversation_id=conversation_id,
            )
        except BaseException as e:
            logger.error(f"Unexpected python error: '{e}'")
            self._chat.update_message_error(
                message_id=message_id,
                error=str(e),
                status=UNKNOWN_ERROR_CODE,
                updated_at=None,
                conversation_id=conversation_id,
            )
        else:
            logger.info("Ollama chat request has finished")
            self._chat.update_message_ok(
                message_id=message_id,
                updated_at=None,
                conversation_id=conversation_id,
            )

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
        conversation_id: ChatConversationID,
        server_key: OllamaFilename,
        model_name: str,
        content: str,
        images: Optional[Sequence[Union[str, bytes]]] = None,
        stream=False,
    ) -> ChatConversationID:
        if self._ollama_chat_runner.running:
            raise ValueError("The ollama chat runner is running")

        message = Message(
            role="user",
            content=content,
            images=tuple(Image(value=img) for img in images) if images else None,
            tool_calls=None,
        )
        request = message.model_dump_json()

        if conversation_id == NOT_FOUND_INDEX:
            cache = self._chat.create_new_chat_stream(title=content, request=request)
            assert 1 == len(cache.messages)
            current_message = cache.messages[0]
            conversation_id = cache.conversation_id
        else:
            cache = self._chat[conversation_id]
            current_message = self._chat.append_chat(conversation_id, request)

        ollama = self._ollamas[server_key]
        model_index = ollama.model_names.index(model_name)
        assert 0 <= model_index < len(ollama.model_names)

        messages: List[Message] = list()
        for msg in cache.messages:
            if not msg.is_ok:
                continue
            messages.append(msg.load_request())
            messages.append(cache.get_merged_response_message(msg.id))

        logger.info(f"Request chat stream: '{content}'")
        try:
            self._ollama_chat_runner(
                conversation_id,
                current_message.id,
                ollama,
                model_name,
                messages,
                stream,
            )
        finally:
            return conversation_id
