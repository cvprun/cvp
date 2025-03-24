# -*- coding: utf-8 -*-

from abc import ABC, abstractmethod
from typing import Optional, TypeVar

from imgui_bundle import imgui

from cvp.config.sections.bases.sidebar import SidebarWindowConfig
from cvp.config.sections.proxies.sidebar import SidebarWidthProxy
from cvp.imgui.begin_child import begin_child
from cvp.imgui.flags.child import BORDERS
from cvp.renderer.context import RendererContext
from cvp.renderer.window.base import WindowBase
from cvp.types.override import override
from cvp.variables import (
    MAX_SIDEBAR_WIDTH,
    MIN_SIDEBAR_WIDTH,
    MIN_WINDOW_HEIGHT,
    MIN_WINDOW_WIDTH,
)
from cvp.widgets.splitter import Splitter

SidebarWidthT = TypeVar("SidebarWidthT", bound=SidebarWindowConfig)


class SidebarWindowInterface(ABC):
    @abstractmethod
    def on_process_sidebar(self) -> None:
        raise NotImplementedError

    @abstractmethod
    def on_process_main(self) -> None:
        raise NotImplementedError


class SidebarWindow(WindowBase[SidebarWidthT], SidebarWindowInterface):
    def __init__(
        self,
        context: RendererContext,
        window_config: SidebarWidthT,
        title: Optional[str] = None,
        closable: Optional[bool] = None,
        flags: Optional[int] = None,
        min_width=MIN_WINDOW_WIDTH,
        min_height=MIN_WINDOW_HEIGHT,
        modifiable_title=False,
        min_sidebar_width=MIN_SIDEBAR_WIDTH,
        max_sidebar_width=MAX_SIDEBAR_WIDTH,
        sidebar_border=False,
    ):
        super().__init__(
            context=context,
            window_config=window_config,
            title=title,
            closable=closable,
            flags=flags,
            min_width=min_width,
            min_height=min_height,
            modifiable_title=modifiable_title,
        )

        self._sidebar_border = sidebar_border
        self._sidebar_width = SidebarWidthProxy(window_config)
        self._sidebar_splitter = Splitter.from_vertical(
            "## VSplitter",
            value_proxy=self._sidebar_width,
            min_value=min_sidebar_width,
            max_value=max_sidebar_width,
        )

    @property
    def sidebar_width(self) -> float:
        value = self.window_config.sidebar_width
        return self._sidebar_splitter.normalize_value(value)

    @sidebar_width.setter
    def sidebar_width(self, value: float) -> None:
        value = self._sidebar_splitter.normalize_value(value)
        self.window_config.sidebar_width = value

    @override
    def on_process(self) -> None:
        child_flags = BORDERS if self._sidebar_border else 0
        if begin_child(
            label="## ChildSidebar",
            width=self.sidebar_width,
            child_flags=child_flags,
        ):
            self.on_process_sidebar()

        imgui.same_line()
        self._sidebar_splitter.do_process()
        imgui.same_line()

        with begin_child("## ChildMain"):
            self.on_process_main()

    @override
    def on_process_sidebar(self) -> None:
        pass

    @override
    def on_process_main(self) -> None:
        pass
