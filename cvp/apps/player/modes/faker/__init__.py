# -*- coding: utf-8 -*-

from collections import OrderedDict
from io import StringIO
from typing import Callable, Final, List, NamedTuple, NewType, Sequence

from faker import Faker
from faker.providers import BaseProvider
from imgui_bundle import imgui

from cvp.apps.player.modes._base import BaseMode
from cvp.assets.fonts.mdi import FILE_QUESTION
from cvp.context.context import Context
from cvp.imgui.begin_child import begin_child_context
from cvp.imgui.combo import combo
from cvp.imgui.fit_size import FIT_SIZE
from cvp.imgui.flags.child import BORDERS, RESIZE_X
from cvp.imgui.flags.focused import CHILD_WINDOWS
from cvp.imgui.flags.input_text import READ_ONLY
from cvp.imgui.input_int import input_int
from cvp.imgui.input_text import input_text
from cvp.imgui.input_text_multiline import input_text_multiline
from cvp.imgui.text_centered import text_centered
from cvp.imgui.widgets.signature import input_signature
from cvp.nodes.ntype import generate_node_path
from cvp.types.override import override
from cvp.variables import NOT_FOUND_INDEX

ProviderName = NewType("ProviderName", str)
ProviderApi = NewType("ProviderApi", str)


class ProviderInfo(NamedTuple):
    name: ProviderName
    apis: List[ProviderApi]
    provider: BaseProvider


def _create_providers(faker: Faker) -> List[BaseProvider]:
    return faker.providers


def _create_providers_map(faker: Faker) -> OrderedDict[ProviderName, ProviderInfo]:
    result = OrderedDict()
    base_provider_key = set(dir(BaseProvider))
    providers = _create_providers(faker)
    providers.sort(key=lambda p: type(p).__module__)
    for provider in providers:
        assert isinstance(provider, BaseProvider)
        module = type(provider).__module__
        name = module.removeprefix("faker.providers.")
        name = name.split(".")[0].capitalize()
        name = name.replace("_", " ")
        provider_name = ProviderName(name)
        apis1 = set(dir(type(provider))) - base_provider_key
        apis2 = filter(lambda x: callable(getattr(faker, x, None)), apis1)
        apis = list(map(lambda x: ProviderApi(x), apis2))
        apis.sort()
        result[provider_name] = ProviderInfo(provider_name, apis, provider)
    return result


def _get_language_locale_codes() -> List[str]:
    result = list()
    for country, languages in BaseProvider.language_locale_codes.items():
        assert isinstance(country, str)
        if isinstance(languages, Sequence):
            for lang in languages:
                result.append(f"{country}_{lang}")
        elif isinstance(languages, str):
            result.append(f"{country}_{languages}")
        else:
            assert False, "Inaccessible section"
    return result


class FakerMode(BaseMode):
    __cvp_mode_name__ = "Faker"
    __cvp_mode_icon__ = FILE_QUESTION

    _MENU_SPLIT_X: Final[int] = 250
    _MENU_CHILD_FLAGS: Final[int] = RESIZE_X | BORDERS

    _APIS_SPLIT_X: Final[int] = 250
    _APIS_CHILD_FLAGS: Final[int] = RESIZE_X

    def __init__(self, context: Context):
        super().__init__(context)
        self._faker = Faker(context.config.faker.locale)
        self._faker.seed_instance(context.config.faker.seed)
        self._providers = _create_providers_map(self._faker)
        self._locales = _get_language_locale_codes()
        self._output = str()

    @property
    def config(self):
        return self.context.config.faker

    @property
    def locale_index(self) -> int:
        try:
            return self._locales.index(self.config.locale)
        except ValueError:
            return NOT_FOUND_INDEX

    @locale_index.setter
    def locale_index(self, value: int) -> None:
        try:
            self.config.locale = self._locales[value]
        except IndexError:
            self.config.locale = str()

    def get_selected_api(self, provider: ProviderName) -> ProviderApi:
        return ProviderApi(self.get_selected_submenu(suffix=str(provider)))

    def set_selected_api(self, provider: ProviderName, api: ProviderApi) -> None:
        self.set_selected_submenu(str(api), suffix=str(provider))

    @override
    def on_process(self) -> None:
        with self.begin_mode_context():
            self.do_child_process()

    def do_child_process(self) -> None:
        with begin_child_context(
            label="Menu",
            size=(self._MENU_SPLIT_X, 0),
            child_flags=self._MENU_CHILD_FLAGS,
        ):
            provider_keys = list(self._providers.keys())
            provider_index = NOT_FOUND_INDEX

            if imgui.begin_list_box("##List", FIT_SIZE):
                try:
                    for i, provider_name in enumerate(provider_keys):
                        provider = self._providers[provider_name]
                        selected = provider_name == self.selected_submenu
                        if selected:
                            provider_index = i
                        if imgui.selectable(str(provider_name), selected)[1]:
                            if self.selected_submenu != str(provider_name):
                                api_name = self.get_selected_api(provider_name)
                                if not api_name or api_name not in provider.apis:
                                    first_api_name = provider.apis[0]
                                    self.set_selected_api(provider_name, first_api_name)
                                self._output = str()
                            self.selected_submenu = str(provider_name)
                            provider_index = i
                finally:
                    imgui.end_list_box()

            if imgui.is_window_focused(CHILD_WINDOWS):
                min_provider_index = 0
                max_provider_index = len(provider_keys) - 1

                if imgui.is_key_pressed(imgui.Key.up_arrow, repeat=True):
                    provider_index = max(min_provider_index, provider_index - 1)
                    provider_name = provider_keys[provider_index]
                    self.selected_submenu = str(provider_name)

                if imgui.is_key_pressed(imgui.Key.down_arrow, repeat=True):
                    provider_index = min(max_provider_index, provider_index + 1)
                    provider_name = provider_keys[provider_index]
                    self.selected_submenu = str(provider_name)

        imgui.same_line()

        with begin_child_context("Main"):
            selected_provider_name = ProviderName(self.selected_submenu)
            if selected_provider := self._providers.get(selected_provider_name):
                self.do_provider_process(selected_provider)
            else:
                text_centered("Please select a item")

    def do_provider_process(self, provider: ProviderInfo) -> None:
        imgui.text(f"Provider : {provider.name}")
        imgui.separator()

        if locale_result := combo("Locale", self.locale_index, self._locales):
            self.locale_index = locale_result.value
            if locale_result.item is not None:
                self._faker.seed_locale(locale_result.item, self.config.seed)
        if seed_result := input_text("Seed", self.config.seed):
            self.config.seed = seed_result.value
            self._faker.seed_instance(seed_result.value)
        if imgui.button("Random seed value"):
            self.config.update_random_seed()
            self._faker.seed_instance(self.config.seed)
        if repeat_result := input_int("Repeat", self.config.repeat):
            self.config.repeat = repeat_result.value
        if separator_result := input_text("Separator", self.config.separator):
            self.config.separator = separator_result.value

        with begin_child_context(
            label="API Menu",
            size=(self._APIS_SPLIT_X, 0),
            child_flags=self._APIS_CHILD_FLAGS,
        ):
            api_index = NOT_FOUND_INDEX

            if imgui.begin_list_box("##List", FIT_SIZE):
                try:
                    for i, api_name in enumerate(provider.apis):
                        selected = api_name == self.get_selected_api(provider.name)
                        if selected:
                            api_index = i
                        if imgui.selectable(str(api_name), selected)[1]:
                            self.set_selected_api(provider.name, api_name)
                            api_index = i
                finally:
                    imgui.end_list_box()

            if imgui.is_window_focused(CHILD_WINDOWS):
                min_api_index = 0
                max_api_index = len(provider.apis) - 1

                if imgui.is_key_pressed(imgui.Key.up_arrow, repeat=True):
                    api_index = max(min_api_index, api_index - 1)
                    selected_api_name = provider.apis[api_index]
                    self.set_selected_api(provider.name, selected_api_name)

                if imgui.is_key_pressed(imgui.Key.down_arrow, repeat=True):
                    api_index = min(max_api_index, api_index + 1)
                    selected_api_name = provider.apis[api_index]
                    self.set_selected_api(provider.name, selected_api_name)

        imgui.same_line()

        with begin_child_context("API Main"):
            selected_api = self.get_selected_api(provider.name)
            api_callable = getattr(self._faker, selected_api, None)
            if api_callable is not None:
                assert callable(api_callable)
                self.do_api_process(api_callable)
            else:
                text_centered("Please select a API")

    def generate(self, api: Callable, *args, **kwargs) -> str:
        buffer = StringIO()
        separator = self.config.escaped_separator
        for _ in range(self.config.repeat):
            data = api(*args, **kwargs)
            if isinstance(data, str):
                buffer.write(data)
            else:
                buffer.write(str(data))
            buffer.write(separator)
        return buffer.getvalue()

    def do_api_process(self, api: Callable) -> None:
        imgui.text(f"API : {api.__name__}")

        sig_name = generate_node_path(api)
        input_signature(sig_name, api)

        if imgui.button("Generate"):
            self._output = self.generate(api)

        imgui.separator()

        with begin_child_context("MainBottom"):
            imgui.text("Output")

            if imgui.button("Copy"):
                imgui.set_clipboard_text(self._output)
            imgui.same_line()
            if imgui.button("Clear"):
                self._output = str()

            input_text_multiline("##Output", self._output, FIT_SIZE, READ_ONLY)
