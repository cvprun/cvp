# -*- coding: utf-8 -*-

from cvp.context.mixins._base import BaseContextMixin


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
        # messages = self._chat.messages(conversation_id)
        ollama = self._ollamas[server_key]
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

    def request(self, message: str, server_key: str, model_name: str) -> None:
        pass
