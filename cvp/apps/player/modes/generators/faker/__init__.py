# -*- coding: utf-8 -*-

from io import StringIO
from typing import Callable, Dict, Final, List, NamedTuple, NewType, Sequence

from faker import Faker
from faker.providers import BaseProvider
from imgui_bundle import imgui

from cvp.apps.player.modes._base import BaseMode
from cvp.context.context import Context
from cvp.imgui.begin_child import begin_child_context
from cvp.imgui.combo import combo
from cvp.imgui.fit_size import FIT_SIZE
from cvp.imgui.flags.child import BORDERS, RESIZE_X
from cvp.imgui.flags.input_text import READ_ONLY
from cvp.imgui.input_int import input_int
from cvp.imgui.input_text import input_text
from cvp.imgui.input_text_multilingual import input_text_multiline
from cvp.imgui.text_centered import text_centered
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


def _create_providers_map(faker: Faker) -> Dict[ProviderName, ProviderInfo]:
    result = dict()
    base_provider_key = set(dir(BaseProvider))
    for provider in _create_providers(faker):
        assert isinstance(provider, BaseProvider)
        module = type(provider).__module__
        name = module.removeprefix("faker.providers.")
        name = name.split(".")[0].capitalize()
        name = name.replace("_", " ")
        provider_name = ProviderName(name)
        apis1 = set(dir(type(provider))) - base_provider_key
        apis2 = filter(lambda x: callable(getattr(faker, x, None)), apis1)
        apis = list(map(lambda x: ProviderApi(x), apis2))
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

    _MENU_SPLIT_X: Final[int] = 250
    _MENU_CHILD_FLAGS: Final[int] = RESIZE_X | BORDERS

    _APIS_SPLIT_X: Final[int] = 250
    _APIS_CHILD_FLAGS: Final[int] = RESIZE_X | BORDERS

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

    @property
    def selected_submenu_api(self) -> str:
        return self.get_selected_submenu(suffix="api")

    @selected_submenu_api.setter
    def selected_submenu_api(self, value: str) -> None:
        self.set_selected_submenu(value, suffix="api")

    @override
    def do_process(self) -> None:
        with self.begin_mode_context():
            self.do_child_process()

    def do_child_process(self) -> None:
        with begin_child_context(
            label="Menu",
            size=(self._MENU_SPLIT_X, 0),
            child_flags=self._MENU_CHILD_FLAGS,
        ):
            if imgui.begin_list_box("##List", FIT_SIZE):
                try:
                    for name, provider in self._providers.items():
                        selected = name == self.selected_submenu
                        if imgui.selectable(str(name), selected)[1]:
                            if self.selected_submenu != str(name):
                                self.selected_submenu_api = str(provider.apis[0])
                                self._output = str()
                            self.selected_submenu = str(name)
                finally:
                    imgui.end_list_box()

        imgui.same_line()

        with begin_child_context("Main"):
            selected_provider_name = ProviderName(self.selected_submenu)
            if selected_provider := self._providers.get(selected_provider_name):
                self.do_provider_process(selected_provider_name, selected_provider)
            else:
                text_centered("Please select a item")

    def do_provider_process(self, name: ProviderName, provider: ProviderInfo) -> None:
        imgui.text(f"Faker : {name}")
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
            if imgui.begin_list_box("##List", FIT_SIZE):
                try:
                    for api_name in provider.apis:
                        selected = api_name == self.selected_submenu_api
                        if imgui.selectable(str(api_name), selected)[1]:
                            self.selected_submenu_api = str(api_name)
                finally:
                    imgui.end_list_box()

        imgui.same_line()

        with begin_child_context("API Main"):
            selected_api = ProviderApi(self.selected_submenu_api)
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
