# -*- coding: utf-8 -*-

from io import StringIO
from typing import Final, Optional

from faker import Faker
from imgui_bundle import imgui

from cvp.apps.player.modes._base import BaseMode
from cvp.assets.fonts.mdi import FILE_QUESTION
from cvp.context.context import Context
from cvp.exceptions.traceback import traceback_exception_string
from cvp.faker.providers import (
    ApiInfo,
    ProviderApi,
    ProviderInfo,
    ProviderName,
    create_providers,
    get_language_locale_codes,
)
from cvp.imgui.begin_child import begin_child_context
from cvp.imgui.combo import combo
from cvp.imgui.fit_size import FIT_HEIGHT, FIT_SIZE
from cvp.imgui.flags.child import BORDERS, RESIZE_X
from cvp.imgui.flags.focused import CHILD_WINDOWS
from cvp.imgui.flags.input_text import READ_ONLY
from cvp.imgui.input_int import input_int
from cvp.imgui.input_text import input_text
from cvp.imgui.input_text_multiline import input_text_multiline
from cvp.imgui.text_centered import text_centered
from cvp.imgui.tooltip import hovered_tooltip_text
from cvp.imgui.widgets.input_arguments import input_arguments
from cvp.inspect.bind import BindCallable
from cvp.types.override import override
from cvp.variables import NOT_FOUND_INDEX


class FakerMode(BaseMode):
    __cvp_mode_name__ = "Faker"
    __cvp_mode_icon__ = FILE_QUESTION

    _MENU_SPLIT_X: Final[int] = 250
    _MENU_CHILD_FLAGS: Final[int] = RESIZE_X | BORDERS

    _APIS_SPLIT_X: Final[int] = 250
    _APIS_CHILD_FLAGS: Final[int] = RESIZE_X

    _error: Optional[BaseException]

    def __init__(self, context: Context):
        super().__init__(context)
        self._faker = Faker(context.config.faker.locale)
        self._faker.seed_instance(context.config.faker.seed)
        self._providers = create_providers(self._faker)
        self._locales = get_language_locale_codes()
        self._output = str()
        self._error = None

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
                                    first_api_name = next(iter(provider.apis.keys()))
                                    self.set_selected_api(provider_name, first_api_name)
                                self._output = str()
                                self._error = None
                            self.selected_submenu = str(provider_name)
                            provider_index = i
                finally:
                    imgui.end_list_box()

            if imgui.is_window_focused(CHILD_WINDOWS):
                min_provider_index = 0
                max_provider_index = len(provider_keys) - 1
                next_provider_index = NOT_FOUND_INDEX

                if imgui.is_key_pressed(imgui.Key.home, repeat=False):
                    next_provider_index = min_provider_index
                if imgui.is_key_pressed(imgui.Key.up_arrow, repeat=True):
                    next_provider_index = max(min_provider_index, provider_index - 1)
                if imgui.is_key_pressed(imgui.Key.down_arrow, repeat=True):
                    next_provider_index = min(max_provider_index, provider_index + 1)
                if imgui.is_key_pressed(imgui.Key.end, repeat=False):
                    next_provider_index = max_provider_index

                if next_provider_index != NOT_FOUND_INDEX:
                    next_provider_name = provider_keys[next_provider_index]
                    self.selected_submenu = str(next_provider_name)
                    self._output = str()
                    self._error = None

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
                next_api_index = NOT_FOUND_INDEX

                if imgui.is_key_pressed(imgui.Key.home, repeat=False):
                    next_api_index = min_api_index
                if imgui.is_key_pressed(imgui.Key.up_arrow, repeat=True):
                    next_api_index = max(min_api_index, api_index - 1)
                if imgui.is_key_pressed(imgui.Key.down_arrow, repeat=True):
                    next_api_index = min(max_api_index, api_index + 1)
                if imgui.is_key_pressed(imgui.Key.end, repeat=False):
                    next_api_index = max_api_index

                if next_api_index != NOT_FOUND_INDEX:
                    next_api_name = list(provider.apis.keys())[next_api_index]
                    self.set_selected_api(provider.name, next_api_name)
                    self._output = str()
                    self._error = None

            menu_window_width = imgui.get_window_width()

        imgui.same_line()
        spacing = imgui.get_style().item_inner_spacing.x
        min_main_window_width = (imgui.calc_item_width() * 0.5) - (spacing * 0.5)
        remain_spacing = imgui.calc_item_width() - menu_window_width - spacing
        main_window_width = max(min_main_window_width, remain_spacing)
        imgui.set_next_window_size((main_window_width, FIT_HEIGHT))

        with begin_child_context("API Main"):
            selected_api = self.get_selected_api(provider.name)
            if api := provider.apis.get(selected_api):
                self.do_api_process(api)
            else:
                text_centered("Please select a API")

    def generate(self, func: BindCallable) -> str:
        buffer = StringIO()
        separator = self.config.escaped_separator
        for _ in range(self.config.repeat):
            data = func()
            if isinstance(data, str):
                buffer.write(data)
            else:
                buffer.write(str(data))
            buffer.write(separator)
        return buffer.getvalue()

    def do_api_process(self, api: ApiInfo) -> None:
        imgui.text(f"API : {api.name}")

        if self.context.debug:
            hovered_tooltip_text(str(api.signature))

        input_arguments(
            function=api.function,
            arguments=api.arguments,
            error_color=self.error_color,
            use_copy=False,
            use_deepcopy=False,
        )

        if imgui.button("Generate"):
            try:
                self._output = self.generate(api.bind())
                self._error = None
            except BaseException as e:
                self._output = str()
                self._error = e

        imgui.separator()

        with begin_child_context("MainBottom"):
            imgui.text("Output")

            if imgui.button("Copy"):
                if self._error is not None:
                    imgui.set_clipboard_text(str(self._error))
                elif self._output:
                    imgui.set_clipboard_text(self._output)
            imgui.same_line()
            if imgui.button("Clear"):
                self._output = str()
                self._error = None

            if self._error is not None:
                self.text_error(str(self._error))
                if self.context.debug:
                    hovered_tooltip_text(traceback_exception_string(self._error))
            else:
                input_text_multiline("##Output", self._output, FIT_SIZE, READ_ONLY)
