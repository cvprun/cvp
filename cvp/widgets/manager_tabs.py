# -*- coding: utf-8 -*-

from typing import Optional

from cvp.renderer.context import RendererContext
from cvp.types.override import override
from cvp.variables import (
    MAX_SIDEBAR_WIDTH,
    MIN_SIDEBAR_WIDTH,
    MIN_WINDOW_HEIGHT,
    MIN_WINDOW_WIDTH,
)
from cvp.widgets.manager import Manager, ManagerWindowConfigT, MenuItemT
from cvp.widgets.tab import TabBar, TabItem


class ManagerTabs(Manager[ManagerWindowConfigT, MenuItemT]):
    def __init__(
        self,
        context: RendererContext,
        window_config: ManagerWindowConfigT,
        title: Optional[str] = None,
        closable: Optional[bool] = None,
        flags: Optional[int] = None,
        min_width=MIN_WINDOW_WIDTH,
        min_height=MIN_WINDOW_HEIGHT,
        modifiable_title=False,
        min_sidebar_width=MIN_SIDEBAR_WIDTH,
        max_sidebar_width=MAX_SIDEBAR_WIDTH,
        tabs_identifier: Optional[str] = None,
        tabs_flags=0,
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
            min_sidebar_width=min_sidebar_width,
            max_sidebar_width=max_sidebar_width,
        )
        self._tabs = TabBar[MenuItemT](
            context=context,
            identifier=tabs_identifier,
            flags=tabs_flags,
        )

    def register(self, item: TabItem[MenuItemT]) -> None:
        self._tabs.register(item)

    @override
    def on_menu(self, key: str, item: MenuItemT) -> None:
        self._tabs.do_process(item)
